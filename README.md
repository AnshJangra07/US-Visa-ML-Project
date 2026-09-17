# US Visa Approval Prediction

An end-to-end Machine Learning and MLOps project that predicts whether a US visa application is likely to be approved or denied. The project includes data ingestion, validation, transformation, model training, evaluation, artifact management, cloud storage, a FastAPI web application, Docker packaging, and AWS CI/CD deployment.


## Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Local Installation](#local-installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Training the Model](#training-the-model)
- [Prediction Workflow](#prediction-workflow)
- [API Reference](#api-reference)
- [Docker](#docker)
- [AWS Deployment and CI/CD](#aws-deployment-and-cicd)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## Project Overview

The application accepts applicant and employment-related information through a web form and returns a predicted visa status. The model works with categorical and numerical features and uses the same preprocessing artifacts during training and inference.

### Input features

- Continent
- Employee education level
- Previous job experience
- Job training requirement
- Number of employees
- Company age
- Employment region
- Prevailing wage
- Wage unit
- Full-time or part-time position

### Prediction output

The application returns one of the following statuses:

- `Visa-approved`
- `Visa Not-Approved`

The historical dataset uses `case_status` as its target column, with source values such as `Certified` and `Denied`.

## Features

- Modular training pipeline with separate components for each ML stage.
- MongoDB integration for source data ingestion.
- Schema-based data validation using `config/schema.yaml`.
- Numerical and categorical feature transformation.
- Configurable model selection using `config/model.yaml`.
- Model evaluation with an acceptance threshold.
- Model and preprocessing artifact management.
- AWS S3 integration for model registry and inference artifacts.
- FastAPI web application with a browser-based prediction form.
- Dockerized runtime environment.
- GitHub Actions workflow for publishing the image to Amazon ECR and running it on EC2.
- Application logging and custom exception handling.

## Architecture

```text
MongoDB dataset
      |
      v
Data ingestion and train/test split
      |
      v
Data validation against schema.yaml
      |
      v
Data transformation and feature engineering
      |
      v
Model training using configured estimators
      |
      v
Model evaluation and acceptance check
      |
      v
Model and preprocessing artifacts -> AWS S3
      |
      v
FastAPI prediction application
      |
      v
Browser form -> prediction -> visa status
```

## Tech Stack

| Area               | Technologies                                      |
| ------------------ | ------------------------------------------------- |
| Language           | Python 3.8+                                       |
| API and web server | FastAPI, Uvicorn, Jinja2                          |
| Data processing    | Pandas, NumPy, SciPy                              |
| Machine learning   | Scikit-learn, XGBoost, CatBoost, Imbalanced-learn |
| Data source        | MongoDB                                           |
| Artifact storage   | AWS S3                                            |
| Frontend           | HTML, CSS, Bootstrap, Jinja2 templates            |
| Packaging          | Setuptools, pip                                   |
| Deployment         | Docker, Amazon ECR, Amazon EC2                    |
| Automation         | GitHub Actions                                    |

## Project Structure

```text
US-Visa-ML-Project/
|
|-- app.py                         # FastAPI application and routes
|-- demo.py                        # Script for running the training pipeline
|-- Dockerfile                     # Container build instructions
|-- requirements.txt               # Python dependencies
|-- setup.py                       # Python package configuration
|-- .env.example                   # Environment variable template
|
|-- config/
|   |-- schema.yaml                # Dataset schema and feature definitions
|   `-- model.yaml                 # Candidate models and hyperparameters
|
|-- us_visa/
|   |-- components/               # Ingestion, validation, transformation, training
|   |-- configuration/             # MongoDB and AWS connection helpers
|   |-- constants/                # Project-wide constants
|   |-- data_access/              # Database access layer
|   |-- entity/                   # Configuration and artifact entities
|   |-- exception/                # Custom exception handling
|   |-- logger/                   # Application logging
|   |-- pipline/                  # Training and prediction pipelines
|   `-- utils/                    # Shared utility functions
|
|-- template/
|   `-- usvisa.html               # Visa prediction form
|-- static/css/style.css          # Frontend styles
|-- artifact/                     # Generated training artifacts
|-- logs/                         # Generated application logs
|-- notebook/                     # EDA and experimentation notebooks
|-- flowcharts/                   # Pipeline diagrams
`-- .github/workflows/aws.yaml    # AWS build and deployment workflow
```

## Prerequisites

- Python 3.8 or newer
- Git
- MongoDB database or MongoDB Atlas connection
- AWS account with access to S3
- Docker, if running the container locally
- AWS ECR and EC2, if using cloud deployment

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/AnshJangra07/US-Visa-ML-Project.git
cd US-Visa-ML-Project
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv visa
.\visa\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
python -m venv visa
visa\Scripts\activate.bat
```

Linux or macOS:

```bash
python3 -m venv visa
source visa/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The repository contains a local virtual environment named `visa` in the development setup. Always run the application with that environment activated, or use its interpreter directly on Windows:

```powershell
.\visa\Scripts\python.exe -m uvicorn app:app --reload --port 8080
```

## Configuration

Copy the example configuration file and fill in the values locally:

```powershell
Copy-Item .env.example .env
```

Example values:

```env
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>/<database>
AWS_ACCESS_KEY_ID=<your-aws-access-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
AWS_DEFAULT_REGION=us-east-1
AWS_S3_BUCKET_NAME=usvisa-ml-model2026
AWS_S3_KEY=model-registry
```

Set the variables in the shell or in the deployment environment before starting the application. Do not commit `.env` or expose AWS credentials in source control.

PowerShell example:

```powershell
$env:MONGODB_URL = "mongodb+srv://<username>:<password>@<cluster>/<database>"
$env:AWS_ACCESS_KEY_ID = "<your-aws-access-key>"
$env:AWS_SECRET_ACCESS_KEY = "<your-aws-secret-key>"
$env:AWS_DEFAULT_REGION = "us-east-1"
```

## Running the Application

Start the FastAPI application from the project root:

```bash
python app.py
```

Or run it through Uvicorn with auto-reload during development:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8080
```

Open the application at:

```text
http://localhost:8080
```

The application exposes static files at `/static` and renders the form from `template/usvisa.html`.

## Training the Model

The training pipeline runs these stages in order:

1. Ingest data from MongoDB.
2. Split the data into train and test datasets.
3. Validate columns and data quality against `config/schema.yaml`.
4. Transform numerical and categorical features.
5. Train configured candidate models from `config/model.yaml`.
6. Evaluate the trained model.
7. Push accepted model artifacts to the configured AWS S3 location.

### Run training through the API

Start the application and open:

```text
http://localhost:8080/train
```

### Run training through the Python script

```bash
python demo.py
```

Training requires a valid MongoDB connection and the AWS configuration needed by the model pusher. Generated local artifacts are stored under `artifact/`, and logs are written under `logs/`.

## Prediction Workflow

The prediction route creates a `USvisaData` object from the submitted form, converts it to a Pandas DataFrame, loads the trained estimator, and returns the prediction:

```text
Form submission
      |
      v
USvisaData
      |
      v
Pandas DataFrame
      |
      v
Preprocessing artifact + trained model
      |
      v
Visa-approved / Visa Not-Approved
```

The prediction model is loaded through the configured S3 model registry. A trained model artifact must therefore be available before submitting a prediction.

## API Reference

### `GET /`

Renders the prediction form.

### `POST /`

Accepts form-encoded prediction data with these fields:

| Field                   | Example    |
| ----------------------- | ---------- |
| `continent`             | `Asia`     |
| `education_of_employee` | `Master's` |
| `has_job_experience`    | `Y`        |
| `requires_job_training` | `N`        |
| `no_of_employees`       | `20000`    |
| `company_age`           | `25`       |
| `region_of_employment`  | `West`     |
| `prevailing_wage`       | `60000`    |
| `unit_of_wage`          | `Year`     |
| `full_time_position`    | `Y`        |

The browser response renders the prediction result in the form page. Errors are returned as a JSON object containing `status` and `error`.

### `GET /train`

Starts the complete training pipeline and returns a success or error response. This endpoint should be protected before being exposed publicly because it starts a potentially expensive training operation.

## Docker

### Build the image

```bash
docker build -t us-visa-prediction .
```

### Run the container

Pass required environment variables at runtime:

```bash
docker run --rm -p 8080:8080 \
  -e MONGODB_URL="<your-mongodb-url>" \
  -e AWS_ACCESS_KEY_ID="<your-aws-access-key>" \
  -e AWS_SECRET_ACCESS_KEY="<your-aws-secret-key>" \
  -e AWS_DEFAULT_REGION="us-east-1" \
  us-visa-prediction
```

Open `http://localhost:8080` after the container starts.

## AWS Deployment and CI/CD

The workflow in `.github/workflows/aws.yaml` runs when code is pushed to the `main` branch.

### Continuous Integration

The CI job:

1. Checks out the repository.
2. Configures AWS credentials.
3. Logs in to Amazon ECR.
4. Builds the Docker image.
5. Pushes the image with the `latest` tag.

### Continuous Deployment

The deployment job runs on a self-hosted EC2 runner. It:

1. Checks out the repository.
2. Configures AWS credentials.
3. Logs in to Amazon ECR.
4. Pulls and runs the latest image.
5. Publishes the application on port `8080`.

### Required GitHub Secrets

Configure these repository secrets before enabling the workflow:

| Secret                  | Purpose                             |
| ----------------------- | ----------------------------------- |
| `AWS_ACCESS_KEY_ID`     | AWS authentication                  |
| `AWS_SECRET_ACCESS_KEY` | AWS authentication                  |
| `AWS_DEFAULT_REGION`    | AWS region, for example `us-east-1` |
| `ECR_REPO`              | Amazon ECR repository name          |
| `MONGODB_URL`           | MongoDB connection string           |

The AWS user or role must have permissions for Amazon ECR and the deployment resources. The S3 bucket used for model artifacts must also be accessible to the application.


## Author

**Ansh Jangra**

This project demonstrates practical work in machine learning, MLOps, FastAPI, cloud storage, Docker, and CI/CD automation.

