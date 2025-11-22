# Sigmavalue Frontend — Production-ready UI (Vite + React + Tailwind + Recharts)

This is a production-ready frontend scaffold for the Sigmavalue Real Estate Chatbot.
It expects the backend to be running at http://127.0.0.1:8000/ (default Django runserver).

## Features
- Clean chat UI with message history
- Summary card, trends chart, and data table
- Responsive layout (desktop + mobile)
- Built with Vite + React + Tailwind CSS + Recharts + Axios

## Run (development)
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start dev server:
   ```bash
   npm run dev
   ```
3. Open http://localhost:3000

## Build (production)
```bash
npm run build
npm run preview
```

## Notes
- Tailwind is pre-configured via `tailwind.config.cjs` and `postcss.config.cjs`.
- API endpoint: POST /api/analyze/ with JSON `{ "query": "Analyze Wakad" }`
