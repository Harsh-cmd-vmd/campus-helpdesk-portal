# CCA 2 — Step-by-step guide in simple language

This project demonstrates the student guide's flow: GitHub → Jenkins → tests → Docker image → Docker Hub → Minikube/Kubernetes → verification.

## 1. Upload the project to GitHub
1. Unzip the project.
2. Create a GitHub repository named `campus-helpdesk-cicd`.
3. In `k8s/deployment.yaml`, replace `DOCKERHUB_USERNAME` with your Docker Hub username.
4. Open a terminal in the project folder and run:
```bash
git init
git add .
git commit -m "Add Campus Helpdesk CI/CD starter"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/campus-helpdesk-cicd.git
git push -u origin main
```
Replace `YOUR_GITHUB_USERNAME`. Sign in using GitHub's supported authentication if prompted.

## 2. Test the app on your computer
Install Python 3.10+ and Git. Then run:
```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest -v
python app.py
```
Open `http://127.0.0.1:5000` and `http://127.0.0.1:5000/health`. Stop the app with Ctrl+C.

## 3. Prepare Docker Hub
Create a Docker Hub account. In its account settings, create an access token. Keep it private; do not put it in source code or GitHub.

## 4. Prepare AWS and Jenkins
Your course guide asks for Jenkins on AWS. Commands depend on your Ubuntu/AMI version, so use the official installation instructions for Java/Jenkins, Git, Python 3, Docker Engine, `kubectl`, and Minikube.
1. Create an Ubuntu EC2 instance with enough memory/CPU for Jenkins and Minikube.
2. Restrict inbound access: SSH only from your IP; Jenkins web access only from your IP or a secure access method. Do not expose Jenkins publicly without protection.
3. Install and start Jenkins, then complete the first-time setup in the browser.
4. In **Manage Jenkins → Plugins**, ensure Pipeline and Git plugins are installed.
5. Make sure the actual Jenkins build user or a dedicated Jenkins agent can run `python3`, `docker`, `kubectl`, and `minikube`.
6. Start Minikube and check `kubectl get nodes` under the same OS account that runs the pipeline. Jenkins often runs as a separate `jenkins` user; that user may not automatically share your SSH user's Minikube profile or kubeconfig. Configure this deliberately. The pipeline fails if Jenkins cannot access the cluster.
7. Check `docker version` and `kubectl get nodes` as the build user.

Running Jenkins and Minikube on one EC2 machine is a learning setup, not a production architecture. Follow any specific setup your teacher requires.

## 5. Add Docker Hub credentials in Jenkins
1. Open **Manage Jenkins → Credentials** and choose the appropriate global credential store.
2. Click **Add Credentials**.
3. Kind: **Username with password**.
4. Username: Docker Hub username.
5. Password: Docker Hub access token.
6. ID: exactly `dockerhub-creds`.
7. Save.

## 6. Create the Jenkins job
1. Jenkins dashboard → **New Item** → enter `campus-helpdesk-pipeline` → choose **Pipeline** → OK.
2. In the Pipeline section choose **Pipeline script from SCM**.
3. SCM: **Git**; Repository URL: your GitHub repository URL.
4. Branch specifier: `*/main` (or your actual branch).
5. Script Path: `Jenkinsfile`.
6. Save → **Build Now** → open the build → **Console Output**.

## 7. What the pipeline stages mean
1. **Checkout:** Jenkins downloads the latest GitHub code.
2. **Build and Test:** installs dependencies and runs unit tests.
3. **Build Docker Image:** packages the app and its dependencies.
4. **Push Image:** uploads the versioned image to Docker Hub.
5. **Deploy to Minikube:** applies Kubernetes YAML and updates the Deployment to this build's image tag.
6. **Verify:** displays Pod, Deployment and Service status.

## 8. Check the app
Run on the machine/account with access to Minikube:
```bash
kubectl get pods
kubectl get deployments
kubectl get services
kubectl rollout status deployment/campus-helpdesk
minikube service campus-helpdesk --url
```
Open the URL from a browser that can reach the host. If it is only reachable from the EC2 machine, use a secure tunnel or your instructor's approved access method. Do not open all ports to the internet. Alternatively:
```bash
kubectl port-forward service/campus-helpdesk 8080:80
```
Then open `http://127.0.0.1:8080` on that same host (or tunnel securely).

## 9. Required second deployment demonstration
Your guide specifically asks for a source-code change after the first successful run.
1. Edit `app.py`, change `Version: v1` to `Version: v2`.
2. Run:
```bash
git add app.py
git commit -m "Update portal version to v2"
git push
```
3. In Jenkins, click **Build Now** again and wait for success.
4. Verify the app and show the new build number/image tag.
5. Capture screenshots: successful Jenkins stages, Docker Hub tags, `kubectl get pods`, `kubectl get services`, and the app showing v2.

## 10. What to submit (from your course guide)
- GitHub repository URL
- `Jenkinsfile`
- `Dockerfile`
- Kubernetes Deployment and Service YAML files
- Screenshots
- Brief README/report explaining project, AWS/Jenkins setup, stages, image push, deployment/access, and the second change

## Common errors
- **Docker permission denied:** the Jenkins build account lacks Docker access; fix the agent/group permissions securely.
- **kubectl cannot connect:** Minikube may be stopped or kubeconfig belongs to a different OS account.
- **Image pull error:** verify Docker Hub username, repository visibility and image tag.
- **Tests fail:** run `python -m unittest -v` locally first.
- **App won't open:** use `kubectl describe pod POD_NAME` and `kubectl logs POD_NAME`.

## Viva questions
- **CI/CD?** Continuous Integration tests/checks code changes; Continuous Delivery/Deployment automates delivery or deployment.
- **Jenkins?** Runs the stages described in Jenkinsfile.
- **Docker?** Packages the app and dependencies consistently.
- **Docker Hub?** Stores container images.
- **Deployment?** Kubernetes object that manages Pods and updates.
- **Service?** Gives a stable network endpoint to reach Pods.
- **Why tests?** They catch basic errors before deployment.
- **How demonstrate a new version?** Change app text, push to GitHub, rerun Jenkins, verify the updated app.
