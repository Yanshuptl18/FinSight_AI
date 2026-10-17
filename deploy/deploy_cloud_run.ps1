# ==============================================================================
# FinSight AI — Automated Minimal-Cost Google Cloud Run Deployment Script (PowerShell)
# ==============================================================================
[CmdletBinding()]
param (
    [string]$ServiceName = "finsight-ai",
    [string]$Region = "us-central1",
    [string]$Cpu = "1",
    [string]$Memory = "2Gi",
    [int]$MinInstances = 0,
    [int]$MaxInstances = 2,
    [int]$Port = 8080,
    [string]$SecretName = "finsight-hf-token"
)

$ErrorActionPreference = "Stop"

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "FinSight AI — Google Cloud Run Minimal-Cost Deployment" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "Region:         $Region"
Write-Host "Service Name:   $ServiceName"
Write-Host "CPU / Memory:   $Cpu vCPU / $Memory"
Write-Host "Min/Max Pods:   $MinInstances (Scale to Zero) / $MaxInstances"
Write-Host "=================================================================="

# Check for gcloud CLI and auto-resolve from LocalAppData if needed
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    $defaultSdkBin = [System.IO.Path]::Combine($env:LOCALAPPDATA, "Google\Cloud SDK\google-cloud-sdk\bin")
    if (Test-Path $defaultSdkBin) {
        $env:PATH = "$defaultSdkBin;$env:PATH"
    }
}

if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: 'gcloud' CLI is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    Write-Host "Or run this deployment inside Google Cloud Shell (https://shell.cloud.google.com)."
    exit 1
}

# Check active project
$projectId = gcloud config get-value project 2>$null
if (-not $projectId -or $projectId -eq "(unset)") {
    Write-Host "ERROR: No Google Cloud project is currently selected." -ForegroundColor Red
    Write-Host "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
}
Write-Host "Active Google Cloud Project: $projectId" -ForegroundColor Green

# 1. Enable required minimal APIs
Write-Host "`n--> Step 1: Enabling required Google Cloud APIs (Cloud Run, Secret Manager, Cloud Build)..." -ForegroundColor Yellow
gcloud services enable `
    run.googleapis.com `
    cloudbuild.googleapis.com `
    secretmanager.googleapis.com `
    artifactregistry.googleapis.com

# 2. Check or create Secret for HF_TOKEN
Write-Host "`n--> Step 2: Checking Secret Manager for $SecretName..." -ForegroundColor Yellow
$secretExists = gcloud secrets describe $SecretName 2>$null
if (-not $secretExists) {
    Write-Host "Secret '$SecretName' does not exist yet in Secret Manager."
    $localHfPath = [System.IO.Path]::Combine($env:USERPROFILE, ".cache\huggingface\token")
    if (Test-Path $localHfPath) {
        Write-Host "Found authenticated Hugging Face token in $localHfPath. Storing securely..." -ForegroundColor Green
        gcloud secrets create $SecretName --data-file=$localHfPath --replication-policy="automatic"
        $secretExists = $true
    } else {
        $hfToken = Read-Host "Enter your Hugging Face Token (HF_TOKEN) [secure input]" -AsSecureString
        $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($hfToken)
        $plainToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
        
        if ($plainToken) {
            $plainToken | gcloud secrets create $SecretName --data-file=- --replication-policy="automatic"
            Write-Host "Created secret '$SecretName'." -ForegroundColor Green
            $secretExists = $true
        } else {
            Write-Host "WARNING: No token entered. Proceeding without HF_TOKEN secret." -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "Secret '$SecretName' already exists in Secret Manager." -ForegroundColor Green
}

# 3. Grant Secret Manager Access to Cloud Run Service Account
Write-Host "`n--> Step 3: Configuring least-privilege IAM permissions for Secret Manager..." -ForegroundColor Yellow
$projectNumber = gcloud projects describe $projectId --format="value(projectNumber)"
$cloudRunSa = "${projectNumber}-compute@developer.gserviceaccount.com"

if ($secretExists) {
    gcloud secrets add-iam-policy-binding $SecretName `
        --member="serviceAccount:${cloudRunSa}" `
        --role="roles/secretmanager.secretAccessor" 2>$null | Out-Null
}

# 4. Build and Deploy container directly from source to Cloud Run
Write-Host "`n--> Step 4: Deploying FinSight AI to Cloud Run from source..." -ForegroundColor Yellow
Write-Host "Note: .gcloudignore ensures only code (~2MB) is uploaded. Datasets are lazily resolved."

$deployArgs = @(
    "run", "deploy", $ServiceName,
    "--source", ".",
    "--region", $Region,
    "--platform", "managed",
    "--allow-unauthenticated",
    "--port", "$Port",
    "--cpu", "$Cpu",
    "--memory", "$Memory",
    "--min-instances", "$MinInstances",
    "--max-instances", "$MaxInstances",
    "--concurrency", "80",
    "--timeout", "300",
    "--set-env-vars", "HF_REPO_ID=Yanshuptl18/finsight-ai-data"
)
if ($secretExists) {
    $deployArgs += "--set-secrets=HF_TOKEN=${SecretName}:latest"
}

& gcloud @deployArgs

Write-Host "`n==================================================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
$serviceUrl = gcloud run services describe $ServiceName --platform managed --region $Region --format="value(status.url)"
Write-Host "Live URL: $serviceUrl" -ForegroundColor Cyan
Write-Host "=================================================================="
