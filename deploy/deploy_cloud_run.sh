#!/usr/bin/env bash
# ==============================================================================
# FinSight AI — Automated Minimal-Cost Google Cloud Run Deployment Script
# ==============================================================================
set -euo pipefail

# Configuration Defaults
SERVICE_NAME="finsight-ai"
REGION="${GCP_REGION:-us-central1}"
CPU="1"
MEMORY="2Gi"
MIN_INSTANCES="0"
MAX_INSTANCES="2"
PORT="8080"
SECRET_NAME="finsight-hf-token"

echo "=================================================================="
echo "FinSight AI — Google Cloud Run Minimal-Cost Deployment"
echo "=================================================================="
echo "Region:         $REGION"
echo "Service Name:   $SERVICE_NAME"
echo "CPU / Memory:   $CPU vCPU / $MEMORY"
echo "Min/Max Pods:   $MIN_INSTANCES (Scale to Zero) / $MAX_INSTANCES"
echo "=================================================================="

# Check for gcloud CLI
if ! command -v gcloud &> /dev/null; then
    echo "ERROR: 'gcloud' CLI is not installed or not in PATH."
    echo "Please install Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    echo "Or run this deployment inside Google Cloud Shell (https://shell.cloud.google.com)."
    exit 1
fi

# Check active project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "")
if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "(unset)" ]; then
    echo "ERROR: No Google Cloud project is currently selected."
    echo "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi
echo "Active Google Cloud Project: $PROJECT_ID"

# 1. Enable required minimal APIs
echo ""
echo "--> Step 1: Enabling required Google Cloud APIs (Cloud Run, Secret Manager, Cloud Build)..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com \
    artifactregistry.googleapis.com

# 2. Check or create Secret for HF_TOKEN
echo ""
echo "--> Step 2: Checking Secret Manager for $SECRET_NAME..."
if ! gcloud secrets describe "$SECRET_NAME" &>/dev/null; then
    echo "Secret '$SECRET_NAME' does not exist yet."
    read -rsp "Enter your Hugging Face Token (HF_TOKEN) [hidden]: " HF_INPUT_TOKEN
    echo ""
    if [ -n "$HF_INPUT_TOKEN" ]; then
        echo -n "$HF_INPUT_TOKEN" | gcloud secrets create "$SECRET_NAME" --data-file=- --replication-policy="automatic"
        echo "Created secret '$SECRET_NAME'."
    else
        echo "WARNING: No token entered. Proceeding without HF_TOKEN secret."
    fi
else
    echo "Secret '$SECRET_NAME' already exists in Secret Manager."
fi

# 3. Grant Secret Manager Access to Cloud Run Service Account
echo ""
echo "--> Step 3: Configuring least-privilege IAM permissions for Secret Manager..."
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")
CLOUD_RUN_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

if gcloud secrets describe "$SECRET_NAME" &>/dev/null; then
    gcloud secrets add-iam-policy-binding "$SECRET_NAME" \
        --member="serviceAccount:${CLOUD_RUN_SA}" \
        --role="roles/secretmanager.secretAccessor" &>/dev/null || true
fi

# 4. Build and Deploy container directly from source to Cloud Run
echo ""
echo "--> Step 4: Deploying FinSight AI to Cloud Run from source..."
echo "Note: .gcloudignore ensures only code (~2MB) is uploaded. Datasets are lazily resolved."

SECRET_FLAG=""
if gcloud secrets describe "$SECRET_NAME" &>/dev/null; then
    SECRET_FLAG="--set-secrets=HF_TOKEN=${SECRET_NAME}:latest"
fi

gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --region "$REGION" \
    --platform managed \
    --allow-unauthenticated \
    --port "$PORT" \
    --cpu "$CPU" \
    --memory "$MEMORY" \
    --min-instances "$MIN_INSTANCES" \
    --max-instances "$MAX_INSTANCES" \
    --concurrency 80 \
    --timeout 300 \
    --set-env-vars="HF_REPO_ID=Yanshuptl18/finsight-ai-data" \
    $SECRET_FLAG

echo ""
echo "=================================================================="
echo "Deployment Complete!"
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --platform managed --region "$REGION" --format="value(status.url)")
echo "Live URL: $SERVICE_URL"
echo "=================================================================="
