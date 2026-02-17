# CI/CD Pipeline Implementation Plan for Azure Project (azd + GitHub Actions)

## Objective

Set up a fully automated, modular CI/CD pipeline for the Azure project using GitHub Actions and azd. The user should only need to run a single setup script and then `azd up` for end-to-end automation. The pipeline must use reusable workflows, OIDC authentication, and robust role assignment for secure, reliable deployments.

---

## Phases & Steps

### 1. Reusable Deployment Workflow

- **File:** `.github/workflows/deploy.yml`
- **Purpose:** Reusable workflow for deployment.
- **Inputs:** `environment` (e.g., dev, prod), `azure_env_name`.
- **Actions:**
  - OIDC login to Azure
  - `azd env select`
  - `azd provision`
  - `azd deploy`
- **Trigger:** `workflow_call` from other workflows

### 2. Continuous Integration Workflow

- **File:** `.github/workflows/ci.yml`
- **Purpose:** Run on PRs to main, run unit tests and Bicep validation (no deploy)
- **Actions:**
  - Checkout code
  - Set up Python, Node.js, Azure CLI
  - Run backend and frontend unit tests
  - Validate Bicep files (`az bicep build` or `azd infra validate`)
- **Trigger:** `pull_request` to `main`

### 3. Dev Deployment Workflow

- **File:** `.github/workflows/deploy-dev.yml`
- **Purpose:** Deploy to dev on push to main
- **Actions:** Calls `deploy.yml` with `environment=dev` and correct `azure_env_name`
- **Trigger:** `push` to `main`

### 4. Prod Deployment Workflow

- **File:** `.github/workflows/deploy-prod.yml`
- **Purpose:** Manual deployment to prod with confirmation
- **Actions:** Calls `deploy.yml` with `environment=prod` and correct `azure_env_name`
- **Trigger:** `workflow_dispatch` (manual), with required confirmation input

### 5. Automated Setup Script

- **File:** `scripts/setup-cicd.sh`
- **Purpose:** One-time setup for CI/CD pipeline
- **Actions:**
  - Detect existing azd App Registrations (Backend & Frontend)
  - Store their Client IDs as GitHub Secrets (`BACKEND_API_CLIENT_ID`, `FRONTEND_SPA_CLIENT_ID`)
  - Create Service Principal for GitHub OIDC
  - Assign Service Principal as Owner of App Registrations (or grant Application.ReadWrite.OwnedBy)

### 6. Postprovision Hook for RBAC

- **File:** `azure.yaml` (postprovision hook)
- **Script:** `infra/hooks/postprovision.sh`
- **Purpose:** Grant "Cosmos DB Built-in Data Contributor" role to current principal (user or CI SPN) after provisioning

---

## Verification Checklist

- [ ] Run `scripts/setup-cicd.sh` and check GitHub Secrets
- [ ] Trigger PR to main: CI runs, no deployment
- [ ] Push to main: Dev deploy runs
- [ ] Manual prod deploy: Confirmation required
- [ ] Run `azd up`: RBAC errors for Cosmos DB are resolved

---

This plan ensures a fully automated, modular, and secure CI/CD pipeline for Azure using GitHub Actions and azd. User setup is minimal and reliability is maximized.
