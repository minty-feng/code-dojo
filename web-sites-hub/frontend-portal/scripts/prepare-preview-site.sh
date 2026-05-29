#!/bin/bash
#
# 仅用于发布打包（package-joketop.sh）：把各子项目 dist 铺平为 /<项目名>/，部署路径不带 dist。
# 本地预览请用 scripts/preview.sh，showcase 指向各子目录下的 dist/。
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${1:-$PROJECT_ROOT/.preview-site}"

copy_dir_contents() {
    local source_dir="$1"
    local target_dir="$2"

    if [ ! -d "$source_dir" ]; then
        echo "⚠️  未找到构建目录: $source_dir"
        return
    fi

    mkdir -p "$target_dir"
    cp -R "$source_dir"/. "$target_dir"/
}

echo "🧱 准备预览/部署目录: $OUTPUT_DIR"
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# 门户主站静态文件
cp "$PROJECT_ROOT"/index.html "$PROJECT_ROOT"/resume.html "$PROJECT_ROOT"/learning.html \
   "$PROJECT_ROOT"/showcase.html "$PROJECT_ROOT"/snippets.html "$PROJECT_ROOT"/diary.html "$PROJECT_ROOT"/speed.html \
   "$PROJECT_ROOT"/fund.html "$PROJECT_ROOT"/invisiblechars.html \
   "$PROJECT_ROOT"/ganwu.html "$PROJECT_ROOT"/wufu.html "$PROJECT_ROOT"/poems.html \
   "$PROJECT_ROOT"/timeline.html "$PROJECT_ROOT"/goals.html "$PROJECT_ROOT"/tianya.html \
   "$PROJECT_ROOT"/journal.html "$PROJECT_ROOT"/plans.html "$PROJECT_ROOT"/calendar.html \
   "$PROJECT_ROOT"/figures.html "$PROJECT_ROOT"/aihistory.html "$OUTPUT_DIR"/ 2>/dev/null || true

cp -R "$PROJECT_ROOT/assets" "$OUTPUT_DIR/"

# 四个前端子项目：部署路径只保留目录名，不带 dist
copy_dir_contents "$PROJECT_ROOT/phd-game/dist" "$OUTPUT_DIR/phd-game"
copy_dir_contents "$PROJECT_ROOT/super-app/dist" "$OUTPUT_DIR/super-app"
copy_dir_contents "$PROJECT_ROOT/debate-competition/dist" "$OUTPUT_DIR/debate-competition"
copy_dir_contents "$PROJECT_ROOT/internship-trends/dist" "$OUTPUT_DIR/internship-trends"

echo "✅ 完成: $OUTPUT_DIR"
