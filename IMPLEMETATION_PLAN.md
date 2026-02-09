# Visual QA Automation Platform - Implementation Plan

## 1. Project Structure
```
visual-qa-app/
├── backend/                # Python FastAPI Backend
│   ├── app/
│   │   ├── api/            # API Routes (Runs, Auth, Projects)
│   │   ├── core/           # Config, Security, DB
│   │   ├── models/         # SQLAlchemy Models
│   │   ├── schemas/        # Pydantic Schemas
│   │   ├── services/       # Business Logic (Diff, Figma, Playwright)
│   │   └── worker.py       # Celery Worker Entrypoint
│   ├── tests/              # Pytest Suite
│   ├── alembic/            # DB Migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Next.js Frontend
│   ├── content/
│   ├── public/
│   ├── src/
│   │   ├── app/            # App Router (Pages)
│   │   ├── components/     # UI Components
│   │   ├── lib/            # Utilities (API client, helpers)
│   │   └── types/          # TypeScript interfaces
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # Orchestration (App, DB, Redis, Worker)
└── README.md
```

## 2. Technology Stack
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide Icons.
- **Backend**: FastAPI, Pydantic v2, SQLAlchemy 2.0 (Async), Alembic.
- **Worker**: Celery + Redis for async tasks (Screenshots, Diffing).
- **Automation**: Playwright (Python).
- **Image Processing**: OpenCV, NumPy, Pillow.
- **Database**: PostgreSQL 16.

## 3. Core Features Implementation Priority

### Phase 1: Foundation (Backend & DB)
- Set up FastAPI with async SQLAlchemy engine.
- Configure Celery with Redis.
- Implement User Auth (JWT).
- Define Database Models: `User`, `Project`, `Run`, `RunItem`, `Issue`.

### Phase 2: Workflow A (Dev vs Design Image)
- **Backend**:
    - Endpoint to create run with URL + Reference Image.
    - Celery Task:
        1. Capture screenshot of URL via Playwright.
        2. Resize/Align images.
        3. Compute Diff (SSIM/Pixel-match + Contour detection).
        4. Generate Artifacts (Diff image, Overlay).
        5. Save results to DB.
- **Frontend**:
    - "New Run" page with URL input + File Upload.
    - Run Details page showing Side-by-Side comparison.

### Phase 3: Workflow B (Dev vs Figma)
- **Backend**:
    - Figma API integration (fetch nodes, images, styles).
    - Logic to map Figma Nodes to HTML Elements (Bounding Box overlap + Text matching).
    - CSS Diffing logic (Computed Styles vs Figma Properties).

### Phase 4: UI Polish & Enhancements
- Interactive specific diff viewer (click to zoom).
- Dashboard with run history.
- Real-time updates via Polling or SSE (Simpler for MVP).

## 4. Key Technical Decisions
- **Storage**: Local filesystem for MVP (`./data/artifacts`), switchable to S3 via env var.
- **Auth**: Simple JWT implementation.
- **AI Layer**: Abstracted interface `BaseAIProvider` with a default `NoOpAIProvider`.

## 5. Next Steps
1. Initialize Git repository.
2. Create `backend/` and `frontend/` skeletons.
3. Write `docker-compose.yml` to spin up Postgres and Redis.
