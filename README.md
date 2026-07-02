# AgentOps Nexus

> **AI COO for Enterprise Agent Ecosystems — One Agent to Govern Every Other Agent**

AgentOps Nexus is an enterprise-grade SaaS platform designed to govern, evaluate, monitor, and optimize AI agents running in an organization. By introducing an intelligent **Supervisor Agent** paired with dedicated safety, quality, and cost governance agents, the platform autonomously observes and enforces policies in real-time.

---

## 🚀 Key Features

*   **Autonomous COO (Supervisor)**: Orchestrates governance workflows, detects anomalies, and automatically resolves common failures.
*   **Safety Shield (Enkrypt AI)**: Integrated real-time checks for hallucinations, toxicity, bias, jailbreak attempts, and PII leaks.
*   **Cost Management**: Track operational token usage, set budget caps, and receive automated recommendations to transition to cheaper model options.
*   **Vector Memory (Qdrant)**: Retain semantic records of past incidents, policy violations, prompt revisions, and conversation traces.
*   **Next.js Glassmorphism UI**: Beautiful, premium dark-mode interface built with Tailwind CSS, ShadCN principles, and responsive components.

---

## 🛠️ Technology Stack

*   **Frontend**: Next.js 14, React 19, TypeScript, Tailwind CSS, Recharts, Zustand.
*   **Backend**: Python, FastAPI, SQLAlchemy (async PostgreSQL), Celery (async task processing), Redis.
*   **AI Engine**: OpenAI, Anthropic Claude, Google Gemini, LiteLLM.
*   **Memory**: Qdrant Vector Database.
*   **Shield**: Enkrypt AI.
*   **DevOps**: Docker, Docker Compose, Kubernetes, Terraform.

---

## 📁 Repository Structure

```
agentops-nexus/
├── apps/
│   ├── web/            # Next.js frontend application
│   └── api/            # FastAPI backend application
├── infra/
│   ├── docker/         # Production Docker config
│   ├── k8s/            # Kubernetes manifest files
│   ├── prometheus/     # Monitoring scraper configuration
│   ├── grafana/        # Provisioned dashboards and datasources
│   ├── terraform/      # Infrastructure as Code
│   └── nginx/          # Production SSL and Reverse proxy setup
├── docs/               # System architecture and deployment guides
└── package.json        # Root workspace configuration
```

---

## ⚡ Quick Start (Local Development)

### Prerequisites
*   Docker & Docker Compose installed.
*   Node.js (v20+) and Python (3.12+).

### Step 1: Clone the repository and copy environments
```bash
cp .env.example .env
```
Fill in your `OPENAI_API_KEY`, `QDRANT_URL`, etc.

### Step 2: Spin up local services
```bash
docker-compose -f docker-compose.dev.yml up --build
```
This commands launches:
*   PostgreSQL Database (`localhost:5432`)
*   Redis Cache (`localhost:6379`)
*   Qdrant Vector DB (`localhost:6333`)
*   FastAPI API Backend (`localhost:8000`)
*   Celery Worker & Beat scheduler
*   Prometheus & Grafana dashboard (`localhost:3001`)

### Step 3: Run migrations and verify endpoints
Run SQLAlchemy database migrations:
```bash
npm run db:migrate
```
Access Swagger API Docs at `http://localhost:8000/api/docs`.

### Step 4: Run the frontend application
Install dependencies and run Next.js development server:
```bash
cd apps/web
npm install
npm run dev
```
Open `http://localhost:3000` to view the platform!
