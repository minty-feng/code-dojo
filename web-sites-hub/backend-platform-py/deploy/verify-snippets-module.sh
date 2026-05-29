#!/usr/bin/env bash
# Verify snippets module files exist before/after deployment.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REQUIRED_FILES=(
    app/core/snippet_seed.py
    app/core/database.py
    app/core/admin.py
    app/main.py
    app/routers/snippets.py
    app/services/snippet_service.py
    app/schemas/snippets.py
    app/repositories/sqlalchemy_repo.py
)

missing=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "缺少: $file"
        missing=1
    fi
done

if ! grep -q "SnippetAdmin" app/core/admin.py; then
    echo "缺少: app/core/admin.py 未注册 SnippetAdmin"
    missing=1
fi

if ! grep -q "snippets.router" app/main.py; then
    echo "缺少: app/main.py 未注册 snippets 路由"
    missing=1
fi

if [ "$missing" -ne 0 ]; then
    echo "snippets 模块不完整，请同步整个 app/ 目录或重新打包部署。"
    exit 1
fi

echo "snippets 模块文件校验通过✅"
