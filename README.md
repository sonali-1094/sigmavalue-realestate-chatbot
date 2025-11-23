##  Demo Video (1–2 minutes)

Watch the demo video here:  
- https://drive.google.com/file/d/10jCI7md_FoS6JNgcKoepCzI9kX2waBkU/view?usp=sharing

# Sigmavalue — Mini Real Estate Analysis Chatbot

- **Project:** React frontend + Django backend
- **Purpose:** Chat-style UI that accepts natural-language queries about localities, returns a short summary, a chart (price/demand trends), and a filtered table extracted from an Excel dataset.

**Quick Overview**
- Backend: Django + Django REST Framework. Loads a preloaded Excel dataset at `backend/data/sample_real_estate.xlsx` and exposes `/api/analyze/` POST endpoint.
- Frontend: React (Vite) + Tailwind + Recharts. Chat UI in `frontend/src`.

**Prerequisites**
- Node.js (v16+ recommended) and npm or yarn
- Python 3.10+ (virtualenv recommended)
- Git (for cloning/sharing)

**Run Locally — Backend**
- From repository root open PowerShell (Windows). Create & activate venv if not already:

```powershell
# from repo root
python -m venv .venv
# PowerShell activation
& .\\.venv\\Scripts\\Activate.ps1
```

- Install backend packages (if you don't have a `requirements.txt` yet, run):

```powershell
pip install Django djangorestframework django-cors-headers pandas openpyxl
```

- Run migrations & start server:

```powershell
cd backend
python manage.py migrate
python manage.py runserver
```

The backend API will be available at `http://127.0.0.1:8000/` and the analyze endpoint at `http://127.0.0.1:8000/api/analyze/`.

**Run Locally — Frontend**
- In a separate terminal:

```bash
cd frontend
npm install      # or `yarn`
npm run dev       # starts Vite dev server (default port 3000)
```

Open `http://localhost:3000` to use the chat UI.

**Sample Queries**
- `Give me analysis of Wakad`
- `Compare Ambegaon Budruk and Aundh demand trends`
- `Show price growth for Akurdi over the last 3 years`

Use the chat input in the UI or POST to the API directly:

```bash
curl -X POST http://127.0.0.1:8000/api/analyze/ -H "Content-Type: application/json" -d '{"query":"Analyze Wakad"}'
```

**Testing**
- Unit tests for backend are in `backend/realchat/tests.py`.

```powershell
cd backend
python manage.py test realchat.tests
```

**Files of Interest**
- Backend: `backend/realchat/views.py`, `backend/realchat/utils.py`, `backend/data/sample_real_estate.xlsx`
- Frontend: `frontend/src/App.jsx`, `frontend/src/components/*`

**Optional / Next Steps (Bonus)**
- Integrate OpenAI or other LLM for real summaries. Add an environment variable `OPENAI_API_KEY` and a small wrapper in the backend that calls the LLM for `summary` (mocking is already allowed).
- Add `requirements.txt` (run `pip freeze > requirements.txt` inside venv) and `package-lock.json` / `yarn.lock` for reproducible installs.
- Add a `Download Data` button that hits a backend endpoint returning a CSV/Excel export.
- Add GitHub Actions workflow to run tests on push.

**Deployment Notes (short)**
- Backend: use Gunicorn + WhiteNoise (or an ASGI server for Django channels). Set `DEBUG=False` and add a secure `SECRET_KEY`.
- Frontend: build with `npm run build` and deploy static files to Netlify/Vercel, or serve the built frontend from a simple static server.

**Demo Video & Submission**
- Record a 1-2 minute demo showing:
   - Starting backend & frontend
   - Entering the three sample queries and showing summary/chart/table
   - (Optional) Download data and LLM summary
- Push code to GitHub and include the link + demo video in the repo README or project submission.

**Contact / Questions**
- If you want, I can also:
   - Generate a `requirements.txt` and a small `Procfile` for Heroku
   - Add a `Download Data` API and frontend button
   - Add CI workflow for tests

---

