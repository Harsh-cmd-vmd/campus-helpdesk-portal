# Campus Helpdesk Portal — CI/CD starter project

A small Flask web application for learning the CCA 2 CI/CD assignment. Includes tests, Dockerfile, Jenkinsfile, and Kubernetes manifests.

**Important:** the supplied CCA 2 guide says to use an existing academic project. This is a new starter project for practice. Ask your teacher whether a new sample project is accepted, or adapt these deployment files to a project you already made.

## Files
- `app.py` — web app
- `test_app.py` — automated tests
- `Dockerfile` — creates the container image
- `Jenkinsfile` — checkout, test, Docker build/push, deploy and verification
- `k8s/` — Kubernetes Deployment and Service
- `STEP_BY_STEP_GUIDE.md` — beginner setup guide

## Test locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest -v
python app.py
```
On Windows, activate with `.venv\\Scripts\\activate`. Open `http://127.0.0.1:5000`.

Before running Jenkins: push to GitHub; replace `DOCKERHUB_USERNAME` in `k8s/deployment.yaml`; create a Jenkins Username/password credential with ID `dockerhub-creds` (Docker Hub username + access token); make sure the Jenkins build user/agent can run Python, Docker, kubectl and access the same running Minikube cluster.
# campus-helpdesk-portal
