# Churn Prediction Platform

Originally built as a university capstone project for Nuu Mobile, this repository is an independently published and sanitized portfolio release. It is not an official Nuu Mobile product and is not affiliated with or endorsed by Nuu Mobile.

This is a full-stack machine learning application for predicting customer churn, generating dashboard visualizations from uploaded data, training multiple models, and surfacing risk insights through a unified web interface.

What makes it stand out is that it goes well beyond model experimentation. The project carries the workflow through data ingestion, preprocessing, persistence, APIs, visualization, and deployment, with Dockerized local setup and an AWS-backed deployment path used during the original capstone.

## Why this project stands out

Most ML projects stop at a notebook. This project turns the model into a usable system: one that accepts uploaded files, adapts to evolving schemas, retrains models, stores results, and turns output into dashboards and decision-support views.

## Key Capabilities

- Built as a full application, with Dockerized local deployment and AWS-oriented environment support
- Generates dashboard graphs directly from user-uploaded data files instead of relying on static sample data
- Supports both XGBoost and a PyTorch MLP, with training and inference exposed through the web app
- Implements dynamic feature expansion, allowing the system to adapt to evolving schemas and new datasets without being locked to a fixed column set
- Predicts which customers are most likely to leave based on user-provided data files, then surfaces the results through threshold-based review and analytics workflows

## Development Notes

- Originally developed as a university capstone project
- OpenAI tools were used during development to accelerate implementation and iteration
- Claude was used during public-release sanitization and polishing

## Core Features

### 1. Batch churn prediction
- Upload customer/device datasets and generate churn predictions in bulk
- Review prediction probabilities in a results table
- Export prediction results to CSV
- Adjust the risk threshold in the UI to redefine which customers are flagged as high risk

<img width="1440" height="813" alt="Screenshot 2026-04-16 at 8 27 23 PM" src="https://github.com/user-attachments/assets/4dbe2b44-ce81-47f1-87e0-27604bc8b5c2" />


### 2. Model training from the web app
- Train an XGBoost model from uploaded data
- Train a PyTorch MLP from uploaded data
- Track training status and progress from the frontend
- Reset or clean up model artifacts when retraining from scratch
- CatBoost and TabNet were also evaluated during development (`backend/catBoost.py`, `backend/tabNet.py`); XGBoost and MLP were selected for production based on performance

<img width="1440" height="813" alt="screenshot 2" src="https://github.com/user-attachments/assets/5977d982-ba98-42df-b027-4bbd9f735857" />
<img width="1440" height="813" alt="screenshot_1 " src="https://github.com/user-attachments/assets/a0664fde-8226-4efa-a6d1-cbae4ad074e0" />

### 3. Analytics dashboard
- View recent prediction batches stored in PostgreSQL
- Explore feature importance for both model families
- Inspect churn-related dashboard views for churn counts, age ranges, activation counts, app usage distribution, carrier distribution, return analysis, usage duration trends, and correlation heatmaps

<img width="1440" height="813" alt="screenshot_3" src="https://github.com/user-attachments/assets/cb8e52d1-be61-48c1-a519-c30ead6c04b0" />
<img width="1440" height="813" alt="Screenshot 2026-04-16 at 8 26 42 PM" src="https://github.com/user-attachments/assets/d2588f4a-9482-4c37-b72c-4fb94c3b204d" />
<img width="1440" height="813" alt="Screenshot 2026-04-16 at 8 26 24 PM" src="https://github.com/user-attachments/assets/10a35249-c4aa-4fec-b9ba-67bed44003b0" />
<img width="745" height="813" alt="Screenshot 2026-04-16 at 8 26 34 PM" src="https://github.com/user-attachments/assets/e1a5fb88-8ed2-4152-9ccc-447480832476" />
<img width="1440" height="813" alt="Screenshot 2026-04-16 at 8 26 50 PM" src="https://github.com/user-attachments/assets/908da1e8-3cb7-419e-b538-88e56d71fa2d" />



### 4. Data pipeline and persistence
- Preprocess uploaded files before training or inference
- Persist prediction batches and device-level data
- Upload separate dashboard datasets for exploratory analytics
- Support flexible columns by normalizing uploaded feature names before storage

## Tech Stack

**Frontend**

- React 19
- Vite
- React Bootstrap
- Recharts
- Chart.js
- D3
- Framer Motion

**Backend**

- Flask
- Pandas
- scikit-learn
- XGBoost (selected model)
- PyTorch MLP (selected model)
- CatBoost, TabNet (evaluated, not deployed)
- Optuna (hyperparameter tuning)
- SHAP
- SQLAlchemy
- psycopg2

**Infrastructure**

- PostgreSQL 15
- Docker Compose

## Architecture

The application is organized as three main services:

1. `frontend/`
   React app for training workflows, prediction review, and dashboard analytics.

2. `backend/`
   Flask API that handles file uploads, preprocessing, model training, batch inference, metrics, and dashboard endpoints.

3. `db`
   PostgreSQL database used for prediction batches, device data, processed features, and dashboard datasets.

High-level flow:

1. A user uploads a CSV/XLSX file from the frontend.
2. The backend preprocesses the dataset through `backend/data_processing.py`.
3. The backend either trains a model or runs batch predictions.
4. Results and metadata are stored in PostgreSQL.
5. The frontend fetches predictions, metrics, feature importance, and dashboard summaries through REST endpoints.

```
Frontend (React)
    ↓
Flask API (REST endpoints)
    ↓
ML Pipeline (XGBoost / MLP)
    ↓
PostgreSQL
```

## Repository Structure

```text
backend/
  app.py                  Flask API and orchestration layer
  data_processing.py      Dataset normalization and preprocessing
  train.py                Training utilities
  db/churn_database.sql   Database schema

frontend/
  src/pages/              Dashboard, predictions, training, settings pages
  src/components/charts/  Reusable chart components

docker-compose.yml        Multi-service local deployment
.env.example              Root environment template
```

## Getting Started

### Prerequisites

- Docker Desktop or Docker Engine with Compose

### 1. Clone the repo

```bash
git clone https://github.com/willzhu16/churn_dashboard.git
cd churn_dashboard
```

### 2. Create environment files

Copy the example environment files and fill in real values as needed:

```bash
cp .env.example .env
cp frontend/.env.docker.example frontend/.env
```

Important variables in `.env`:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASS`
- `DB_ROW_LIMIT`
- `XGB_TOTAL_TRIALS`
- `MLP_TOTAL_EPOCHS`
- `ENVIRONMENT`
- `BUILD_MODE`

Recommended local Docker settings:

```env
ENVIRONMENT=docker
BUILD_MODE=docker
DB_HOST=db
DB_PORT=5432
```

The frontend Docker example points the UI to:

```env
VITE_API_URL=http://127.0.0.1:5050
```

### 3. Start the stack

```bash
docker compose build
docker compose up
```

### 4. Open the app

- Frontend: `http://localhost:4173`
- Backend API: `http://localhost:5050`

### Local development (without Docker)

If you have PostgreSQL running locally, you can run the services directly.

**Backend:**
```bash
cd backend
pip install -r requirements.txt
# configure .env with your local DB credentials
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Notable API Surface

Some representative backend routes:

- `GET /health`
- `POST /train_model`
- `POST /train_MLP_model`
- `POST /predict_batch`
- `POST /predict_batch_MLP`
- `GET /predictions`
- `GET /feature_importance`
- `GET /feature_importance_MLP`
- `POST /upload_dashboard_data`
- `GET /dashboard_data`
- `GET /correlation_matrix`

## Current Limitations

- Training progress is partly estimated and should be treated as a user-friendly proxy rather than exact job-state reporting.
- Environment setup is Docker-first; non-Docker local development is not fully documented or verified.
- Automated tests and CI are not yet included in this repository.
- Some dashboard visualizations assume a semi-structured dataset (e.g., device-level or telecom-style features). While the preprocessing pipeline supports flexible schemas, certain charts rely on expected feature patterns and may require adaptation for completely different domains.

## What I’d Improve Next

- Add automated backend and frontend test coverage
- Add API documentation
- Replace approximate progress indicators with more robust job tracking
- Add authentication and tighter upload validation for production use
- Improve experiment management and model artifact versioning
- Add CI/CD for linting, tests, and deployment

## My Contributions

This project was originally developed as part of a team capstone project. I was responsible for the core system design and the majority of the implementation, particularly on the backend and machine learning side.

My contributions include:

- Designing and implementing the backend API (Flask) for training, prediction, and data workflows
- Building the machine learning pipeline, including preprocessing, feature handling, and model integration (XGBoost, PyTorch MLP)
- Designing and integrating the PostgreSQL database schema for prediction batches and device-level data
- Implementing end-to-end workflows for model training, batch prediction, and result persistence
- Handling system integration across the ML pipeline, backend services, and database

I had limited involvement in the frontend during initial development, but later contributed to integration and minor updates to support the training and prediction workflows.

I also refined and sanitized the project into a portfolio-ready version.

## What this project demonstrates

- Designing a production-style ML system, not just a model
- Integrating training and inference into a unified workflow
- Building data pipelines that handle evolving feature schemas
- Presenting model outputs for real decision-making
