# CODEMED EOB → 835 Demo

This repository contains a demo for converting paper explanation of benefits (EOB) documents into ANSI X12 835 remittance files.

## Quick start (development)

1. Launch the repository in a GitHub Codespace or clone it locally.
2. Install dependencies:
   - **Backend:** run `pip install -r backend/requirements.txt`.
   - **Frontend:** run `cd frontend && npm install`.
3. Start the backend server:
   - Run `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`.
4. Start the frontend:
   - Run `cd frontend && npm run dev` (from the repository root or another terminal).
5. Open the frontend in your browser (default http://localhost:3000), upload a demo EOB (no PHI) and export an 835 file.

## Deployment

A sample `infra/cloudrun.sh` script is included to build and deploy the backend and frontend images to Google Cloud Run. Before running it, configure `GCP_PROJECT_ID` and `GCP_REGION` as environment variables or set up secrets in GitHub Actions.

## Environment

- Copy `.env.example` to `.env` and update the values for your environment.
- The variable `NEXT_PUBLIC_BACKEND_URL` must point to your running backend (for local development it defaults to http://localhost:8000).
