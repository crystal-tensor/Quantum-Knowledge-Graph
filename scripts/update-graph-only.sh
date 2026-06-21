#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/crystal-tensor/Quantum-Knowledge-Graph.git}"
BRANCH="${BRANCH:-main}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET_DIR="${1:-${PROJECT_DIR}/graph}"
HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:6122/api/health}"

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

echo "[graph-update] repo: ${REPO_URL}"
echo "[graph-update] branch: ${BRANCH}"
echo "[graph-update] target: ${TARGET_DIR}"

git clone --depth 1 --filter=blob:none --sparse --branch "${BRANCH}" "${REPO_URL}" "${TMP_DIR}"
git -C "${TMP_DIR}" sparse-checkout set graph graph_data.json

if [[ -d "${TMP_DIR}/graph" ]]; then
  SOURCE_DIR="${TMP_DIR}/graph"
elif [[ -f "${TMP_DIR}/graph_data.json" ]]; then
  SOURCE_DIR="${TMP_DIR}/graph"
  mkdir -p "${SOURCE_DIR}"
  cp "${TMP_DIR}/graph_data.json" "${SOURCE_DIR}/graph_data.json"
else
  echo "[graph-update] ERROR: repository does not contain graph/ or graph_data.json" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"
rsync -av --delete "${SOURCE_DIR}/" "${TARGET_DIR}/"

echo "[graph-update] synced graph files"
if command -v curl >/dev/null 2>&1; then
  echo "[graph-update] health:"
  curl -fsS "${HEALTH_URL}" || true
  echo
fi
