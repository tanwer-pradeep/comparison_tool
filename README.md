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
