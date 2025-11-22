import re
import io
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .utils import load_dataset
from .llm import generate_summary_from_data

# Correct dataset path
DATA_FILE = "data/sample_real_estate.xlsx"
DF = load_dataset(DATA_FILE)

# ---------------------------------------------
# Extract two localities for comparison
# ---------------------------------------------
def extract_localities(query):
    text = query.lower()
    parts = re.split("compare|and|vs|versus|with", text)
    locs = [p.strip() for p in parts if p.strip()]
    return locs[:2]


# ---------------------------------------------
# Find locality names present in the query by
# checking dataset area names (robust substring match)
# ---------------------------------------------
def find_localities_in_query(query):
    q = query.lower()
    areas = sorted(DF['area'].unique(), key=lambda x: -len(x))
    found = []
    for a in areas:
        a_low = a.lower()
        if a_low in q:
            found.append(a)
    return found

# ---------------------------------------------
# Return locality dataset
# ---------------------------------------------
def locality_data(loc):
    temp = DF[DF["area"].str.lower() == loc.lower()]
    if temp.empty:
        return None
    return {
        "year": temp["year"].tolist(),
        "price": temp["price"].tolist(),
        "demand": temp["demand"].tolist(),
        "table": temp.to_dict(orient="records")
    }

# ---------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------
@api_view(["POST"])
def analyze(request):
    query = request.data.get("query", "").lower().strip()

    # =====================================================
    # 1️⃣ COMPARISON MODE
    # =====================================================
    if "compare" in query:
        # Try to detect locality names robustly from the dataset
        locs = find_localities_in_query(query)
        if len(locs) < 2:
            # fallback to the older extraction heuristic
            locs = extract_localities(query)
        if len(locs) < 2:
            return Response({"error": "Please specify two localities to compare."})

        loc1, loc2 = locs[0], locs[1]
        d1 = locality_data(loc1)
        d2 = locality_data(loc2)

        if not d1 or not d2:
            return Response({"error": "One of the localities not found in dataset."})

        # build payload for the LLM helper
        payload = {
            "localities": [loc1, loc2],
            "chartData": {
                loc1: {"price": d1["price"], "demand": d1["demand"], "year": d1["year"]},
                loc2: {"price": d2["price"], "demand": d2["demand"], "year": d2["year"]},
            },
            "tableData": {loc1: d1["table"], loc2: d2["table"]},
        }

        summary = generate_summary_from_data(payload, mode="comparison")

        return Response({
            "type": "comparison",
            "summary": summary,
            "localities": [loc1, loc2],
            "chartData": {
                loc1: d1,
                loc2: d2
            },
            "tableData": {
                loc1: d1["table"],
                loc2: d2["table"]
            }
        })

    # =====================================================
    # 2️⃣ PRICE GROWTH MODE
    # =====================================================
    if "price growth" in query or "last" in query:
        # detect locality by checking dataset area names in the query
        match_years = re.search(r"last (\d+) years", query)
        years = int(match_years.group(1)) if match_years else 3

        locs = find_localities_in_query(query)
        if not locs:
            # try a simple regex fallback
            match_loc = re.search(r"for ([a-zA-Z ]+)", query)
            if match_loc:
                loc = match_loc.group(1).strip()
            else:
                return Response({"error": "Cannot detect the locality."})
            temp = DF[DF["area"].str.lower() == loc.lower()]
            if temp.empty:
                return Response({"error": "Locality not found."})
        else:
            loc = locs[0]
            temp = DF[DF["area"].str.lower() == loc.lower()]

        temp = temp.sort_values("year").tail(years)

        payload = {
            "locality": loc,
            "chartData": {"year": temp["year"].tolist(), "price": temp["price"].tolist(), "demand": temp["demand"].tolist()},
            "tableData": temp.to_dict(orient="records"),
        }

        summary = generate_summary_from_data(payload, mode="price_growth")

        return Response({
            "type": "price_growth",
            "summary": summary,
            "chartData": {
                "year": temp["year"].tolist(),
                "price": temp["price"].tolist(),
                "demand": temp["demand"].tolist()
            },
            "tableData": temp.to_dict(orient="records")
        })

    # =====================================================
    # 3️⃣ SINGLE LOCALITY ANALYSIS (DEFAULT)
    # =====================================================
    # Default single-locality analysis: detect area name from query
    locs = find_localities_in_query(query)
    if locs:
        loc = locs[0]
    else:
        loc = query.replace("analyze", "").replace("analysis of", "").strip()

    temp = DF[DF["area"].str.lower() == loc.lower()]

    if temp.empty:
        return Response({"error": "Locality not found."})

    payload = {
        "locality": loc,
        "chartData": {"year": temp["year"].tolist(), "price": temp["price"].tolist(), "demand": temp["demand"].tolist()},
        "tableData": temp.to_dict(orient="records"),
    }

    summary = generate_summary_from_data(payload, mode="single")

    return Response({
        "type": "single",
        "summary": summary,
        "chartData": {
            "year": temp["year"].tolist(),
            "price": temp["price"].tolist(),
            "demand": temp["demand"].tolist()
        },
        "tableData": temp.to_dict(orient="records")
    })


@api_view(["POST"])
def download_data(request):
    """Download dataset as CSV. Accepts optional POST body with `areas` (list)
    or `area` (string) to filter the exported rows.
    """
    payload = request.data or {}
    areas = payload.get('areas') or payload.get('area')

    df = DF
    if areas:
        if isinstance(areas, str):
            areas = [areas]
        areas_lower = [a.lower() for a in areas]
        df = DF[DF['area'].str.lower().isin(areas_lower)]

    csv_str = df.to_csv(index=False)
    # Return as downloadable CSV
    response = HttpResponse(csv_str, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_real_estate.csv"'
    return response
