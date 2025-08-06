# 📄 repo-flatten

> **Transform your codebase into AI-ready documentation in seconds**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

`repo-flatten` is a powerful Python tool designed to streamline the process of preparing codebases for AI training data and LLM interactions. Whether you're feeding code to GPT models, creating documentation, or analyzing project structures, this tool compiles your entire repository into a single, comprehensive document with intelligent filtering and professional formatting.

**Perfect for:**
- 🤖 **AI/LLM Training**: Prepare clean, structured training data
- 📚 **Code Documentation**: Generate comprehensive project overviews  
- 🔍 **Code Analysis**: Get a bird's-eye view of project structure
- 📤 **Code Sharing**: Share entire codebases in a readable format
- 🎓 **Educational**: Understand project architectures at a glance

## ✨ Features

### 🌳 **Smart Structure Analysis**
- **Hierarchical Tree View**: Beautiful ASCII tree representation of your project
- **Intelligent Filtering**: Skip binaries, media files, and build artifacts automatically
- **Custom Patterns**: Include/exclude files with glob patterns (`*.py`, `*.js`, etc.)

### 📄 **Multiple Output Formats**
- **📝 Text Format**: Clean, readable `.txt` files
- **📋 Word Documents**: Professional `.docx` with proper formatting
- **🎨 Customizable Styling**: Monospace fonts for code, proper headers

### ⚡ **Advanced Filtering**
- **File Type Filtering**: Ignore images, videos, binaries by default
- **Directory Exclusion**: Skip `node_modules`, `.git`, `__pycache__`, etc.
- **Path-Based Exclusions**: Precisely exclude directories by relative path (NEW!)
- **Pattern Matching**: Include only specific file types with wildcards
- **Settings Control**: Toggle inclusion of config files
- **Scope Limiting**: Process only specific directories
- **Content Toggle**: Skip file contents entirely with `--no-content` to generate structure-only output

### 🛡️ **Robust & Reliable**
- **Error Handling**: Graceful handling of permission errors and encoding issues
- **Large File Support**: Configurable file size limits
- **Encoding Fallbacks**: Multiple encoding attempts for international files
- **Dry Run Mode**: Preview what will be processed before generating output

### 🎛️ **Developer-Friendly**
- **Verbose Logging**: Detailed progress information
- **Flexible CLI**: Intuitive command-line interface
- **Configuration Files**: JSON-based settings for team consistency
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Installation

```bash
# Clone and run locally
git clone https://github.com/daniel-carvajal/repo-flatten.git
cd repo-flatten
pip install -r requirements.txt
```

### Basic Usage

```bash
# Document current directory
repo2txt

# Document specific repository
repo2txt -r /path/to/your/project -o project_docs.txt

# Generate Word document with verbose output
repo2txt -r /path/to/project -o documentation.docx --verbose
```

### Development Commands

```bash
# Generate repo2txt output from the library source
make repo2txt-lib

# Seed the test-repo directory with test data
make seed

# Run automated tests with pytest
make test

# Clean generated test files and output
make clean
```

## 🎯 Filter Logic & Behavior

Understanding how filters work together ensures predictable results every time.

### **Processing Order (What Gets Applied When)**
```
Repository Files
      ↓
1. 🚫 Hard Exclusions (always applied)
   • Output file, .env files, .git/, node_modules/, __pycache__/, hidden files
      ↓
2. 📁 Directory Scope Flags (optional)
   • --scope-to: Process only this directory (excludes all others, then applies file filters like --include-files "*.py")
   • --exclude-dir: Remove these directories (keeps everything else, combines with any flags like --ignore-types .log)
      ↓
3. ✅ File Whitelist Flags (optional - overrides defaults)
   • --include-files: ONLY process files matching these patterns (works within directory scope set by step 2's --scope-to/--exclude-dir, excludes all others). This means we can filter purely by pattern, limit to a directory then filter by pattern, or exclude directories then filter by pattern.
      ↓
4. ❌ File Blacklist Flags (applied to remaining files)
   • --ignore-files: Skip specific filenames
   • --ignore-types: Skip file extensions  
   • --ignore-settings: Skip config files
      ↓
Final Output
```

### **Key Rules**
| Rule | Behavior | Override? |
|------|----------|-----------|
| **Hard exclusions** | Always blocked | ❌ Never |
| **`--scope-to`** | Limits scope to one directory | ❌ No |
| **`--include-files`** | Whitelist mode - ONLY these files | ⚠️ Overrides ignore-types defaults |
| **Directory filters** | Remove/keep entire directories | ✅ Use `none` to disable |
| **File filters** | Remove individual files | ✅ Use `none` to disable |

### **Filter Interactions**
- 🎯 **Include takes precedence**: `--include-files` overrides `--ignore-types` defaults
- 🔄 **Combines logically**: `--include-files "*.py" --exclude-dir tests` = "Python files but not in test directories"
- 🛡️ **Security first**: `.env` files are always excluded regardless of other settings
- 💡 **Use `none`**: Disable specific filters with `--ignore-types none` or `--exclude-dir none`

## 📋 Usage Patterns

### **🆕 Path-Based Directory Exclusions**
NEW! Enhanced `--exclude-dir` now supports both directory names AND relative paths:

```bash
# Traditional: Exclude all directories named "android" everywhere
repo2txt --exclude-dir android -o no_android.txt

# NEW: Exclude only specific android directories by path
repo2txt --exclude-dir example/android FabricExample/android -o selective.txt

# Mixed: Combine path and name exclusions
repo2txt --exclude-dir example/android ios windows -o clean_output.txt

# Precise control for complex projects
repo2txt --scope-to third-party/react-native-pdf \
         --exclude-dir example/android example/ios \
         --no-content -o structure.txt
```

**Path-based exclusion rules:**
- `--exclude-dir android` → excludes ALL directories named "android"
- `--exclude-dir example/android` → excludes ONLY the android directory inside example
- `--exclude-dir src/tests ios` → excludes src/tests path AND all ios directories
- Paths are relative to the processing root (`--scope-to` or repo root)
- Cross-platform compatible (works with both `/` and `\` separators)

### **Whitelist Approach (Specific Files Only)**
```bash
# Only Python files across entire repo
repo2txt --include-files "*.py" -o python_only.txt

# Only config files
repo2txt --include-files "*.json" "*.yaml" "*.toml" -o configs.txt

# Only documentation files
repo2txt --include-files "*.md" "*.rst" "*.txt" -o docs_only.txt
```

### **Scope + Filter (Directory First, Then Refine)**
```bash
# All files in src/ directory only
repo2txt --scope-to src -o src_all.txt

# Python files in src/ directory only
repo2txt --scope-to src --include-files "*.py" -o src_python.txt

# Everything in src/ except specific test subdirectories
repo2txt --scope-to src --exclude-dir src/tests src/__tests__ -o src_no_tests.txt
```

### **Blacklist Approach (Everything Except...)**
```bash
# Everything except images/videos (uses default excludes + custom)
repo2txt --ignore-types .jpg .png .mp4 -o no_media.txt

# Everything except specific test directories
repo2txt --exclude-dir tests/__tests__ example/tests -o no_tests.txt

# All file types but skip settings files
repo2txt --ignore-types none --ignore-settings -o code_only.txt
```

### **Mixed Strategies**
```bash
# Python/JS files, but skip specific test directories
repo2txt --include-files "*.py" "*.js" --exclude-dir src/tests example/tests -o code_no_tests.txt

# Everything in backend/ except logs and temp files
repo2txt --scope-to backend --ignore-files "*.log" "*.tmp" -o backend_clean.txt

# Config files but not from node_modules or specific paths
repo2txt --include-files "*.json" "*.yaml" --exclude-dir node_modules example/config -o clean_configs.txt
```

### **Debugging & Analysis**
```bash
# See what would be processed without generating output
repo2txt --dry-run --verbose

# Check specific directory structure with path exclusions
repo2txt --scope-to src --exclude-dir src/tests --dry-run --verbose

# Test file patterns with path-based exclusions
repo2txt --include-files "*.py" --exclude-dir example/android --dry-run
```

### **Structure-Only Output**
```bash
# Output only the directory/file tree (no code)
repo2txt --no-content -o structure_only.txt

# Combine with precise path filtering
repo2txt --scope-to src --exclude-dir src/tests src/__pycache__ --no-content -o tree_src.txt
```

## ⚙️ Configuration

### **Command-Line Reference**

| Flag | Behavior | Example |
|------|----------|---------|
| `-r PATH` | Repository path | `-r /path/to/repo` |
| `-o FILE` | Output file (.txt/.docx) | `-o docs.docx` |
| `--scope-to DIR` | **Scope to directory only** | `--scope-to src` |
| `--include-files PATTERNS` | **Whitelist: ONLY these files** | `--include-files "*.py" "*.js"` |
| `--exclude-dir DIRS/PATHS` | **Remove directories (names or paths)** | `--exclude-dir tests example/android` |
| `--ignore-files FILES` | Skip specific files | `--ignore-files README.md` |
| `--ignore-types EXTS` | Skip file extensions | `--ignore-types .log .tmp` |
| `--ignore-settings` | Skip config files | `--ignore-settings` |
| `--verbose` | Show processing details | `--verbose` |
| `--dry-run` | Preview only (no output) | `--dry-run` |
| `--no-content` | Skip file contents and output only the folder/file structure | `--no-content` |

**Use `none` to disable**: `--ignore-types none`, `--exclude-dir none`

### **🆕 Enhanced --exclude-dir Examples**

```bash
# Traditional name-based exclusions (existing behavior)
--exclude-dir android ios windows

# NEW: Path-based exclusions for precise control
--exclude-dir example/android FabricExample/ios

# Mixed: Combine both approaches
--exclude-dir android example/tests src/__pycache__

# Complex project filtering
--scope-to third-party/react-native-pdf \
--exclude-dir example/android example/ios FabricExample/android
```

### Configuration File (`config.json`)

Customize default behavior with a JSON configuration file:

```json
{
  "image_extensions": [".png", ".jpg", ".jpeg", ".gif", ".svg"],
  "video_extensions": [".mp4", ".avi", ".mov", ".mkv"],
  "document_extensions": [".pdf", ".doc", ".docx"],
  "archive_extensions": [".zip", ".tar", ".gz", ".7z"],
  "executable_extensions": [".exe", ".dll", ".bin"],
  "settings_extensions": [".ini", ".cfg", ".conf", ".json", ".yaml"],
  "additional_ignore_types": [".lock", ".pyc", ".cache"],
  "default_output_file": "output.txt",
  "max_file_size_mb": 10
}
```

## 🎨 Output Examples

### Text Output Format
```
Repository Documentation
========================

Directory/File Tree -->

my-project/
├── src/
│   ├── main.py
│   ├── utils/
│   │   ├── helpers.py
│   │   └── constants.py
│   └── tests/               # Excluded with --exclude-dir src/tests
│       └── test_main.py
├── README.md
└── requirements.txt

<-- Directory/File Tree

File Contents -->

[File Begins] src/main.py
#!/usr/bin/env python3
"""Main application entry point."""

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
[File Ends] src/main.py

...
```

### Word Document Features
- 📝 Professional formatting with proper fonts
- 🎯 Monospace code blocks for readability
- 📋 Clear section headers and navigation
- 🎨 Consistent styling throughout

## 🔄 Quick Reference

### **Most Common Use Cases**
```bash
# Basic documentation
repo2txt                                    # Current directory, all files
repo2txt --no-content                      # Tree structure only, no file content

# Language-specific
repo2txt --include-files "*.py"             # Python only
repo2txt --include-files "*.py" "*.js"      # Python + JavaScript

# Directory-focused  
repo2txt --scope-to src                     # Only src/ directory
repo2txt --scope-to api --include-files "*.py"  # Python files in api/ only

# Clean output (no build artifacts) - NEW path-based exclusions
repo2txt --exclude-dir node_modules dist build example/android  # Skip common build dirs + specific paths
repo2txt --ignore-types none --exclude-dir tests example/tests  # All files except specific test dirs

# Configuration files
repo2txt --include-files "*.json" "*.yaml" "*.toml"  # Config files only

# Debugging with enhanced exclusions
repo2txt --exclude-dir example/android --dry-run --verbose  # See what path exclusions match
```

## 🧪 Testing

The project includes a comprehensive test suite and automation tools:

```bash
# Seed test data (creates test-repo directory structure)
make seed

# Run all tests with pytest
make test

# Clean up test artifacts and generated files
make clean

# Generate documentation for the library itself
make repo2txt-lib
```

### Test Structure
The testing system creates a sample repository structure for validation:

```
test-repo/
├── README.md
├── ios/
│   └── AppDelegate.swift
└── src/
    ├── utils.py
    ├── android/
    │   └── MainActivity.kt
    └── ios/
        └── helper.swift
```

Tests validate various filtering scenarios:
- Excluding specific directories by name (e.g., all `ios` folders)
- Excluding specific directories by path (e.g., only `src/android`)
- Including only specific subdirectories (e.g., `test-repo/src/ios`)
- File pattern matching (e.g., only `*.py` files)
- Mixed name and path-based exclusions

## 🤝 Use Cases

### 🤖 **AI/ML Training Data**
Perfect for creating clean, structured datasets for training code-aware AI models:

```bash
# Clean Python training data, excluding specific test directories
repo2txt --include-files "*.py" --exclude-dir tests example/tests src/__tests__ -o python_training.txt

# Multi-language dataset with precise platform exclusions
repo2txt --include-files "*.py" "*.js" "*.java" "*.cpp" \
         --exclude-dir android/build ios/build example/android \
         -o multilang_training.txt
```

### 📚 **Documentation Generation**
Generate comprehensive project documentation:

```bash
# Full project overview excluding platform-specific examples
repo2txt --exclude-dir node_modules .git example/android example/ios -o project_overview.docx

# Developer onboarding docs with precise filtering
repo2txt --scope-to src docs --exclude-dir src/tests docs/examples \
         --ignore-types .pyc .log -o onboarding.txt
```

### 🔍 **Code Analysis**
Analyze codebases for patterns and structure:

```bash
# Security audit preparation with path-based exclusions
repo2txt --include-files "*.py" "*.js" "*.php" \
         --exclude-dir tests example/tests vendor/tests \
         -o security_audit.txt

# Architecture review excluding build artifacts and examples
repo2txt --scope-to src --exclude-dir src/tests src/examples src/build \
         -o architecture_review.docx
```

## 🐛 Troubleshooting

| Issue | Solution | Command |
|-------|----------|---------|
| **Files missing from output** | Use verbose to see what's excluded | `repo2txt --verbose --dry-run` |
| **Path exclusions not working** | Check relative paths and use verbose | `--exclude-dir example/android --verbose` |
| **Permission denied errors** | Check which directories are inaccessible | `repo2txt --verbose` |
| **Too many files** | Use whitelist approach | `--include-files "*.py" "*.js"` |
| **Wrong directory scope** | Verify scope-to path | `--scope-to src --dry-run` |
| **Unexpected file types** | Check default ignore list | `--ignore-types none --verbose` |

### **Understanding Output**
- **Verbose shows**: Which files are processed, permission errors, file counts, path vs name exclusion matches
- **Dry-run shows**: What would be included without generating output
- **File paths**: Relative to repo root (or scope-to if specified)
- **Path matching**: Shows "Excluding (path match)" vs "Excluding (name match)" in verbose mode

## 🔄 Version History

### v2.1.0 (Latest)
- 🎯 **NEW: Path-based directory exclusions** - `--exclude-dir` now supports relative paths
- 🔧 Enhanced cross-platform path normalization
- 📊 Improved verbose logging for debugging exclusions
- 🛡️ Maintained backward compatibility with existing name-based exclusions

### v2.0.0
- ✨ Added `--include-files` pattern matching
- 🛡️ Enhanced error handling and encoding support
- 📊 Added verbose mode and dry-run functionality
- 🎨 Improved DOCX formatting with monospace fonts
- ⚡ Better performance for large repositories
- 🔧 Comprehensive configuration options
- 🌳 Added `--no-content` flag to output only the folder structure without file contents

### v1.x.x
- 📄 Basic text and DOCX output
- 🌳 Directory tree generation
- 🚫 Basic file filtering

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 **Bug Reports**
- Use the issue tracker with detailed reproduction steps
- Include sample repository structure if possible
- Provide verbose output logs (especially for path exclusion issues)

### ✨ **Feature Requests**
- Check existing issues before creating new ones
- Provide clear use cases and expected behavior
- Consider submitting a pull request!

### 🔧 **Development Setup**

```bash
# Clone the repository
git clone https://github.com/yourusername/repo2txt.git
cd repo2txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
black src/
flake8 src/
```

### 📝 **Pull Requests**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a pull request with a clear description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [python-docx](https://python-docx.readthedocs.io/) for Word document generation
- Inspired by the need for better AI training data preparation
- Thanks to all contributors and users providing feedback

## 📬 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/yourusername/repo2txt/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/repo2txt/discussions)
- 📖 **Documentation**: [Wiki](https://github.com/yourusername/repo2txt/wiki)

---

<div align="center">

**Made with ❤️ for developers who love clean, organized code**

[⭐ Star this repo](https://github.com/yourusername/repo2txt) | [🐛 Report Bug](https://github.com/yourusername/repo2txt/issues) | [✨ Request Feature](https://github.com/yourusername/repo2txt/issues)

</div>
