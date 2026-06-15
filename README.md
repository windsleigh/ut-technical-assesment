# get-app — CI/CD security demo
 
A small Flask API with a CI/CD pipeline built on GitHub Actions. The point of this repo is the pipeline and its security checks, not the app itself.
 
## What the app does
 
`get-app` reports basic stats about the machine it runs on. It has three endpoints:
 
- `GET /health` — returns `{"status": "ok"}`. Used for health checks.
- `GET /getHeader` — returns current CPU %, memory %, and process count.
- `GET /getProcs` — returns the list of running processes (PID, CPU, memory, name).
It reads these stats from standard Linux tools (`ps`, `free`, `/proc`), so it runs on Linux or in the container below — not natively on macOS or Windows.
 
## Run it locally
 
You need Docker.
 
```bash
cd backend/get-app
docker build -t get-app .
docker run --rm -p 5000:5000 get-app
```
 
Then in another terminal:
 
```bash
curl localhost:5000/health
curl localhost:5000/getProcs
```
 
To run the tests:
 
```bash
cd backend/get-app
pip install -r requirements.txt -r requirements-dev.txt
pytest
```
 
## Published image
 
Every push to `main` publishes the container image to the GitHub Container Registry:
 
```bash
docker pull ghcr.io/windsleigh/ut-technical-assesment-non-ai:latest
```
 
## How the pipeline works
 
There are two workflows in `.github/workflows/`.
 
**CI (`ci.yml`)** runs on every push and pull request, with four jobs:
 
- **lint-test** — runs `ruff` (lint) and `pytest` (tests).
- **sast** — runs Bandit to scan the Python code for insecure patterns.
- **secret-scan** — runs Gitleaks to check for secrets committed to git.
- **image-scan** — builds the Docker image and scans it with Trivy for known vulnerabilities.
**Deploy (`deploy.yml`)** runs on pushes to `main`. It builds the image and pushes it to GHCR, tagged with both the commit SHA and `latest`.
 
Findings from Bandit and Trivy are uploaded to the repo's **Security → Code scanning** tab.
 
## Security choices and why
 
The pipeline checks four separate layers, because each one catches a different kind of problem:
 
- **Bandit (code scanning)** — finds insecure patterns in the Python code, such as unsafe subprocess calls.
- **Gitleaks (secret scanning)** — stops keys, passwords, and tokens from leaking into git history.
- **Trivy (image scanning)** — finds known CVEs in the container's OS packages and dependencies.
- **Dependabot** — opens pull requests to update outdated or vulnerable Python packages, GitHub Actions, and the Docker base image.
A few choices also keep the pipeline itself secure:
 
- **Least-privilege tokens.** Each workflow grants only the `permissions` it needs — for example, only the deploy job can write packages.
- **No stored secrets.** Publishing to GHCR uses the built-in `GITHUB_TOKEN`, so there are no long-lived credentials to manage.
- **Hardened image.** The container uses a slim base image pinned to a specific Python version, installs only what it needs, and runs as a non-root user.
## Reproduce a pipeline run
 
Push any commit or open a pull request and watch the **Actions** tab — the CI jobs run automatically. Pushing to `main` also runs the deploy job and publishes a new image to GHCR.
