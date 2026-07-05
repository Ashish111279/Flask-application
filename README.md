# Flask CI/CD Demo

This repository includes a simple Flask application with both Jenkins and GitHub Actions CI/CD pipelines.

## Repository contents

- `app.py` - simple Flask application.
- `requirements.txt` - runtime dependencies.
- `requirements-dev.txt` - test dependencies.
- `tests/test_app.py` - pytest-based unit tests.
- `Jenkinsfile` - Jenkins pipeline definition.
- `.github/workflows/python-ci-cd.yml` - GitHub Actions workflow.
- `scripts/deploy_staging.sh` - simulated staging deployment.
- `scripts/deploy_production.sh` - simulated production deployment.

## Jenkins CI/CD Pipeline

The `Jenkinsfile` defines a declarative pipeline with these stages:

1. Build: installs dependencies from `requirements.txt`
2. Test: runs `pytest`
3. Deploy: deploys to a staging environment when the `main` branch is built

### Jenkins prerequisites

- Jenkins installed and running.
- Python 3 installed on the Jenkins node.
- `pytest` installed or available via `requirements-dev.txt`.
- Email notification configured in Jenkins if using the `mail` step.

### Jenkins setup notes

- Add this repository to Jenkins as a Pipeline job.
- Configure the Pipeline to use the `Jenkinsfile` in the repository root.
- Set build triggers to poll SCM or use GitHub webhooks on `main` branch changes.

## GitHub Actions CI/CD Workflow

The workflow is defined in `.github/workflows/python-ci-cd.yml` and includes:

- Install dependencies
- Run tests with `pytest`
- Deploy to staging when changes are pushed to `staging`
- Deploy to production when a release is tagged

### GitHub Secrets

Use repository secrets to store deployment credentials and tokens:

- `STAGING_DEPLOY_KEY`
- `PROD_DEPLOY_KEY`

### Trigger rules

- `main` and `staging` branch pushes run the build/test pipeline.
- `staging` pushes run the staging deploy job after tests pass.
- Releases tagged in GitHub run the production deploy job.

## Running locally

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

3. Run tests:

```bash
pytest
```

4. Start the app:

```bash
python app.py
```

5. Open the HTML UI in your browser:

```bash
http://localhost:5000/ui
```

## School Records API

The Flask app now exposes CRUD endpoints for school records:

- `GET /records` — list all student records
- `GET /records/<id>` — retrieve a single record
- `POST /records` — create a new record
- `PUT /records/<id>` — update an existing record
- `DELETE /records/<id>` — delete a record

Example create payload:

```json
{
  "name": "Alice King",
  "grade": "12",
  "section": "C",
  "marks": {
    "math": 88,
    "science": 91,
    "english": 85
  }
}
```

## Docker

Build the container image:

```bash
docker build -t flask-ci-cd-demo .
```

Run the container:

```bash
docker run -p 5000:5000 flask-ci-cd-demo
```

## Notes

This repository is a demo scaffolding for CI/CD. The deploy scripts simulate deployment by copying files into local directories. In a real environment, replace the deploy scripts with actual staging or production deployment commands.

## Docker Support

The included `Dockerfile` builds the Flask app into a container image and runs it on port `5000`. Use this for local integration testing and to standardize the staging/production runtime.
