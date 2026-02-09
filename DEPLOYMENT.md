# Deployment Guide

This application consists of three main components that need to be deployed:
1.  **Frontend**: Next.js (React) application.
2.  **Backend**: FastAPI (Python) application.
3.  **Database & Worker**: PostgreSQL database, Redis, and Celery worker.

**Important**: GitHub Pages supports **static sites only**. It cannot run Python code, databases, or background workers. Therefore, we recommend a split deployment strategy.

---

## Option 1: The "Production-Grade" Path (Recommended)
**Free Tier Available** via Render.com and Vercel.

### 1. Database & Backend (Render.com)
Render is ideal because it supports `docker-compose` or individual services easily.

#### A. Create Database (PostgreSQL)
1.  Sign up at [render.com](https://render.com/).
2.  Click **New +** -> **PostgreSQL**.
3.  Name: `visual-qa-db`.
4.  Copy the `Internal DB URL` (for backend) and `External DB URL` (for local access).

#### B. Create Redis (for Celery)
1.  Click **New +** -> **Redis**.
2.  Name: `visual-qa-redis`.
3.  Copy the `Internal Redis URL`.

#### C. Deploy Backend API
1.  Click **New +** -> **Web Service**.
2.  Connect your GitHub repo: `tanwer-pradeep/comparison_tool`.
3.  **Root Directory**: `backend`.
4.  **Runtime**: Python 3.
5.  **Build Command**: `pip install -r requirements.txt && python -m playwright install chromium && python -m playwright install-deps`
6.  **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
7.  **Environment Variables**:
    *   `SQLALCHEMY_DATABASE_URI`: (Paste Internal DB URL from Step A)
    *   `CELERY_BROKER_URL`: (Paste Internal Redis URL from Step B)
    *   `CELERY_RESULT_BACKEND`: (Paste Internal Redis URL from Step B)
    *   `SECRET_KEY`: (Generate a random string)
    *   `BACKEND_CORS_ORIGINS`: `["https://your-frontend-url.vercel.app"]` (Update this after deploying frontend)

#### D. Deploy Celery Worker
1.  Click **New +** -> **Background Worker**.
2.  Connect the same GitHub repo.
3.  **Root Directory**: `backend`.
4.  **Runtime**: Python 3.
5.  **Build Command**: `pip install -r requirements.txt && python -m playwright install chromium && python -m playwright install-deps`
6.  **Start Command**: `celery -A app.worker.celery_app worker --loglevel=info`
7.  **Environment Variables**: Same as Backend API.

---

### 2. Frontend (Vercel)
Vercel is the creators of Next.js and offers the best hosting experience.

1.  Sign up at [vercel.com](https://vercel.com/).
2.  Click **Add New...** -> **Project**.
3.  Import `tanwer-pradeep/comparison_tool`.
4.  **Root Directory**: Edit and select `frontend`.
5.  **Environment Variables**:
    *   `NEXT_PUBLIC_API_URL`: `https://your-backend-service-name.onrender.com/api/v1`
6.  Click **Deploy**.

---

## Option 2: Frontend on GitHub Pages (Static Only)
**Limitations**:
*   No Server-Side Rendering (SSR).
*   No `next/image` optimization (unless using a custom loader).
*   **Still requires a separate Backend host** (like Render/Heroku/AWS).

### Steps
1.  **Update Configuration**:
    In `frontend/next.config.mjs`, enable static export:
    ```javascript
    const nextConfig = {
      output: 'export',
      images: { unoptimized: true }, // Required for GH Pages
    };
    export default nextConfig;
    ```

2.  **Update Scripts**:
    In `frontend/package.json`:
    ```json
    "scripts": {
      "build": "next build",
      "deploy": "gh-pages -d out"
    }
    ```

3.  **Install Deploy Tool**:
    ```bash
    cd frontend
    npm install --save-dev gh-pages
    ```

4.  **Deploy**:
    ```bash
    npm run build
    npm run deploy
    ```

This will push the static files to a `gh-pages` branch, providing a URL like `https://tanwer-pradeep.github.io/comparison_tool/`.
