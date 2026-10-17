# FinSight AI — Google Cloud Run Minimal-Cost Deployment Guide

This guide details the exact architecture, resource sizing, free-tier quotas, and deployment instructions for hosting FinSight AI on Google Cloud Run with minimal practical cost.

---

## 1. Minimal-Cost Architecture Overview

FinSight AI is packaged as an ephemeral, stateless Docker container running on Google Cloud Run. Datasets are not baked into the Docker image, ensuring fast build times and a tiny image footprint (< 300 MB).

```text
┌────────────────────────────────────────────────────────┐
│                   USER WEB BROWSER                     │
└───────────────────────────┬────────────────────────────┘
                            │ HTTPS (Port 443)
                            ▼
┌────────────────────────────────────────────────────────┐
│              GOOGLE CLOUD RUN SERVICE                  │
│  • Scale-to-Zero (min-instances: 0, $0 when idle)      │
│  • Max instances: 2 (hard ceiling against spikes)      │
│  • 1 vCPU / 2 GiB RAM (optimal memory profile)         │
│  • Ephemeral in-memory tmpfs cache                     │
└──────────────┬───────────────────────────┬─────────────┘
               │                           │
               │ Authenticated API         │ Secret Mount
               ▼                           ▼
┌──────────────────────────────┐ ┌────────────────────────┐
│      HUGGING FACE HUB        │ │ GOOGLE SECRET MANAGER  │
│  Yanshuptl18/finsight-ai-data│ │  Secret:               │
│  • 86 files (5.67 GB total)  │ │  finsight-hf-token     │
│  • Lazy on-demand download   │ └────────────────────────┘
└──────────────────────────────┘
```

---

## 2. Google Cloud Free-Tier & Cost Risk Analysis

### Cloud Run Monthly Free Allowances (Per Billing Account)

| Metric | Monthly Free Tier Allowance | FinSight AI Configuration | Projected Monthly Cost |
|:---|:---|:---|:---|
| **Requests** | First 2,000,000 requests free | Typical portfolio use: ~5,000 &ndash; 50,000 | **$0.00** |
| **Compute (vCPU-seconds)** | 360,000 vCPU-seconds free (~100 hours of 1-vCPU active runtime) | Scale-to-zero when idle | **$0.00** (within free tier) |
| **Memory (GiB-seconds)** | 180,000 GiB-seconds free (~25 hours of 2-GiB active runtime) | Scale-to-zero when idle | **$0.00** (within free tier) |
| **Network Egress** | First 1 GB egress free to North America per month | Streamlit web traffic: ~500 MB &ndash; 1.5 GB | **$0.00 &ndash; $0.15** |
| **Cloud Build** | 120 build-minutes free per day | Build takes ~2 &ndash; 3 minutes | **$0.00** |
| **Artifact Registry** | 500 MB storage free per month | Compressed image: ~220 MB | **$0.00** |
| **Secret Manager** | 6 secret versions active free per month | 1 secret version (`HF_TOKEN`) | **$0.00** |

> [!IMPORTANT]
> **Cost Control Guarantee**: Setting `--min-instances 0` ensures that Google Cloud will completely shut down all container instances when no requests are being processed, reducing idle compute costs to **$0.00**.

### Selected Region: `us-central1` (Iowa) or `us-east1` (South Carolina)
Both regions qualify for Google Cloud Tier 1 pricing and full free-tier eligibility.

---

## 3. Pre-Deployment Prerequisites

Before running the deployment commands:

1. **Google Cloud Account**: A standard Google Cloud account with an active project and linked billing account (required by Google to activate Cloud Run, even for free-tier usage).
2. **Hugging Face Account & Read Token**:
   - Access to dataset repository: `Yanshuptl18/finsight-ai-data`
   - Generate token at: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) with `Read` permission.
3. **Google Cloud CLI (`gcloud`)**:
   - Install from [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
   - Alternatively, open [Google Cloud Shell](https://shell.cloud.google.com) which has `gcloud`, `git`, and `docker` pre-installed.

---

## 4. Step-by-Step Deployment Instructions

### Step 1: Authenticate with Google Cloud

```bash
gcloud auth login
```
*(Your web browser will prompt you to log into your Google account and grant permissions).*

### Step 2: Set Your Google Cloud Project

```bash
# List your available projects
gcloud projects list

# Set the active project
gcloud config set project YOUR_PROJECT_ID
```

### Step 3: Enable Required Free APIs

```bash
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com \
    artifactregistry.googleapis.com
```

### Step 4: Create Secret for Hugging Face Token

```bash
# Create the secret without exposing token in command line history
echo -n "hf_your_actual_token_here" | gcloud secrets create finsight-hf-token \
    --data-file=- \
    --replication-policy="automatic"
```

### Step 5: Grant Cloud Run Access to the Secret

```bash
PROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)")
CLOUD_RUN_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud secrets add-iam-policy-binding finsight-hf-token \
    --member="serviceAccount:${CLOUD_RUN_SA}" \
    --role="roles/secretmanager.secretAccessor"
```

### Step 6: Deploy to Cloud Run

From the root of `FinSight_AI/`:

```bash
gcloud run deploy finsight-ai \
    --source . \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --cpu 1 \
    --memory 2Gi \
    --min-instances 0 \
    --max-instances 2 \
    --concurrency 80 \
    --timeout 300 \
    --set-env-vars="HF_REPO_ID=Yanshuptl18/finsight-ai-data" \
    --set-secrets="HF_TOKEN=finsight-hf-token:latest"
```

*Note:* Cloud Build will automatically build the container image using the root `Dockerfile` and `.gcloudignore`. The deployment completes in approximately 2 to 3 minutes and outputs the live HTTPS service URL.

---

## 5. Automated Deployment Scripts

For one-command automated deployment:

- **Linux / macOS / Cloud Shell**:
  ```bash
  chmod +x deploy/deploy_cloud_run.sh
  ./deploy/deploy_cloud_run.sh
  ```
- **Windows PowerShell**:
  ```powershell
  .\deploy\deploy_cloud_run.ps1
  ```

---

## 6. How to Update, Stop, or Delete the Service

### Redeploy Updates

When you make changes to the code or README:
```bash
gcloud run deploy finsight-ai --source . --region us-central1
```

### Pause Service (Scale to 0 Instances)

To prevent any incoming traffic from spinning up an instance:
```bash
gcloud run services update finsight-ai --region us-central1 --max-instances 0
```

### Resume Service

```bash
gcloud run services update finsight-ai --region us-central1 --max-instances 2
```

### Delete Service & Clean Up Resources

To completely delete the Cloud Run service and remove all associated charges:
```bash
# Delete Cloud Run service
gcloud run services delete finsight-ai --region us-central1 --quiet

# Delete secret from Secret Manager
gcloud secrets delete finsight-hf-token --quiet

# Optional: Delete container images from Artifact Registry
gcloud artifacts repositories delete cloud-run-source-deploy --location us-central1 --quiet
```
