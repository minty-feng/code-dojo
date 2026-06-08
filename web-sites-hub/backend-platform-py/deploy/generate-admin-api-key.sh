#!/usr/bin/env bash
# 单独生成 ADMIN_API_KEY 并打印（不修改任何文件）
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GREEN='\033[0;32m'
NC='\033[0m'

# shellcheck disable=SC1091
source "$SCRIPT_DIR/print-deploy-hints.sh"
print_admin_api_key_hint
echo -e "${GREEN}完成。${NC}"
