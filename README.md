# Visual QA Automation Platform

A full-stack web application for automated visual regression testing, comparing hosted web apps against design references (images or Figma).

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Quick Start (Docker)
1. **Clone the repository** (if not already)
2. **Start the application**:
   ```bash
   docker-compose up --build
   ```
3. **Access the App**:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Development Setup

#### Backend
1. Navigate to `backend/`:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Run database migrations:
   ```bash
   alembic upgrade head
   ```
3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Start Celery worker:
   ```bash
   celery -A app.worker.celery_app worker --loglevel=info
   ```

#### Frontend
1. Navigate to `frontend/`:
   ```bash
   cd frontend
   npm install
   ```
2. Run the development server:
   ```bash
   npm run dev
   ```

## 🏗 Architecture

- **Backend**: FastAPI (Python), SQLAlchemy (Async), Pydantic v2.
- **Frontend**: Next.js 14, Tailwind CSS, TypeScript.
- **Worker**: Celery + Redis for background processing (Playwright screenshots, OpenCV diffs).
- **Database**: PostgreSQL.
- **Diff Engine**: SSIM + Contour Detection via OpenCV/Scikit-Image.

## 📝 Workflows

1. **URL vs Image**:
   - User inputs URL and uploads a reference image.
   - System captures screenshot of URL.
   - System compares screenshot vs reference.
   - Displays side-by-side view and highlights differences.

2. **URL vs Figma** (Coming Soon):
   - User inputs URL and Figma Node URL.
   - System fetches high-res image from Figma API.
   - Compares against live site.

## 🛠 Project Structure
- `backend/app`: Core application logic.
- `backend/app/services`: Business logic (Diff, Playwright).
- `frontend/src/app`: Next.js App Router pages.
- `data/artifacts`: Storage for screenshots and diff overlays.

## ☁️ Hosting on GitHub

### 1. Push Code to GitHub
Since this is an initialized Git repository, you can push it to GitHub easily:
1. Create a **new repository** on GitHub (do not initialize with README/gitignore).
2. Run the following commands:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/visual-qa-app.git
   git branch -M main
   git push -u origin main
   ```

### 2. CI/CD Pipeline
A GitHub Actions workflow is included in `.github/workflows/ci.yml`. It will automatically:
- Run backend tests (Pytest)
- Build the frontend (Next.js)
- Runs on every Push to `main` and Pull Request.

### 3. Secrets Management
For the CI to pass fully or if you deploy via Actions, ensure you add repository secrets for sensitive env vars (though the current CI uses service containers with default creds for testing).

