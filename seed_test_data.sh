#!/bin/bash

set -e  # Stop on error
ROOT_DIR="test-repo"

echo "🌱 Seeding test directory: $ROOT_DIR"
rm -rf "$ROOT_DIR"
mkdir -p "$ROOT_DIR"

# Top-level ios folder
mkdir -p "$ROOT_DIR/ios"
echo "// Top-level iOS file" > "$ROOT_DIR/ios/AppDelegate.swift"

# Nested ios folder inside src
mkdir -p "$ROOT_DIR/src/ios"
echo "// Nested iOS helper" > "$ROOT_DIR/src/ios/helper.swift"

# Other folders
mkdir -p "$ROOT_DIR/src/android"
echo "// Android MainActivity" > "$ROOT_DIR/src/android/MainActivity.kt"

mkdir -p "$ROOT_DIR/src"
echo "# Utilities" > "$ROOT_DIR/src/utils.py"

echo "# Project README" > "$ROOT_DIR/README.md"

echo "✅ Test directory structure seeded."
