#!/bin/bash
###############################################################################
# SessionStart hook — make the Isaac Sim Terraform (05-isaac-sim/01-deployment)
# deployable from a Claude Code on the web session.
#
# This repo is mostly Markdown, but 05-isaac-sim/01-deployment is real
# Terraform. Two things stop a vanilla `terraform init` from working in the
# web sandbox, and this hook fixes both:
#
#   1. Terraform isn't installed in the container.
#   2. The network policy BLOCKS registry.terraform.io (403), so providers
#      can't be fetched the normal way. releases.hashicorp.com IS allowed,
#      so we download the AWS provider from there into a filesystem mirror
#      and point Terraform at it via ~/.terraformrc.
#
# Idempotent and safe to re-run. Web-only. Does NOT touch AWS — applying is
# still a manual, credential-gated step (see 05-isaac-sim/01-deployment).
###############################################################################
set -euo pipefail

# Only run in the remote (web) environment.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

TF_VERSION="1.13.4"          # >= 1.10 (native S3 state locking) per versions.tf
AWS_PROVIDER_VERSION="5.100.0" # satisfies the repo's ~> 5.40 constraint
MIRROR_DIR="${HOME}/tf-mirror"
ARCH="linux_amd64"

log() { echo "[session-start] $*"; }

# --- 1. Terraform CLI -------------------------------------------------------
if command -v terraform >/dev/null 2>&1; then
  log "terraform already present: $(terraform version | head -1)"
else
  log "installing Terraform ${TF_VERSION}"
  tmp="$(mktemp -d)"
  curl -fsSL -o "${tmp}/terraform.zip" \
    "https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_${ARCH}.zip"
  ( cd "${tmp}" && unzip -o -q terraform.zip )
  install -m0755 "${tmp}/terraform" /usr/local/bin/terraform 2>/dev/null \
    || { mkdir -p "${HOME}/.local/bin" && install -m0755 "${tmp}/terraform" "${HOME}/.local/bin/terraform"; }
  rm -rf "${tmp}"
  log "installed $(terraform version | head -1)"
fi

# Make ~/.local/bin usable this session if we fell back to it.
if ! command -v terraform >/dev/null 2>&1; then
  export PATH="${HOME}/.local/bin:${PATH}"
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "${CLAUDE_ENV_FILE:-/dev/null}"
fi

# --- 2. AWS provider filesystem mirror (registry.terraform.io is blocked) ---
provider_path="${MIRROR_DIR}/registry.terraform.io/hashicorp/aws"
provider_zip="${provider_path}/terraform-provider-aws_${AWS_PROVIDER_VERSION}_${ARCH}.zip"
if [ -f "${provider_zip}" ]; then
  log "aws provider ${AWS_PROVIDER_VERSION} already mirrored"
else
  log "mirroring aws provider ${AWS_PROVIDER_VERSION} from releases.hashicorp.com"
  mkdir -p "${provider_path}"
  curl -fsSL -o "${provider_zip}" \
    "https://releases.hashicorp.com/terraform-provider-aws/${AWS_PROVIDER_VERSION}/terraform-provider-aws_${AWS_PROVIDER_VERSION}_${ARCH}.zip"
  log "mirrored to ${provider_zip}"
fi

# --- 3. Terraform CLI config -> use the mirror ------------------------------
cat > "${HOME}/.terraformrc" <<EOF
provider_installation {
  filesystem_mirror {
    path    = "${MIRROR_DIR}"
    include = ["registry.terraform.io/*/*"]
  }
}
EOF
# Persist the CLI config location for the rest of the session.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export TF_CLI_CONFIG_FILE=${HOME}/.terraformrc" >> "${CLAUDE_ENV_FILE}"
fi
export TF_CLI_CONFIG_FILE="${HOME}/.terraformrc"
log "wrote ${HOME}/.terraformrc (filesystem_mirror -> ${MIRROR_DIR})"

# --- 4. Smoke-test: provider resolves + config validates --------------------
DEPLOY_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}/05-isaac-sim/01-deployment"
if [ -d "${DEPLOY_DIR}" ]; then
  log "validating ${DEPLOY_DIR}"
  # -backend=false: validate without the S3 backend (it needs a real bucket).
  terraform -chdir="${DEPLOY_DIR}" init -backend=false -input=false -no-color >/dev/null
  terraform -chdir="${DEPLOY_DIR}" validate -no-color
fi

log "ready. To deploy you still need valid AWS credentials; see 05-isaac-sim/01-deployment/README.md"
