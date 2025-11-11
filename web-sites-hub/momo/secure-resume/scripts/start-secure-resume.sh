#!/usr/bin/env bash

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -x "./target/release/secure_resume" ]]; then
  echo "Building secure-resume (release)..."
  cargo build --release
fi

echo "Starting secure-resume..."
RUST_LOG=info nohup ./target/release/secure_resume > secure-resume.log 2>&1 &
echo "secure-resume started (pid $!), logging to $(pwd)/secure-resume.log"

