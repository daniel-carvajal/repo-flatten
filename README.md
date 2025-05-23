# 📄 repo2txt

> **Transform your codebase into AI-ready documentation in seconds**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/repo2txt.svg)](https://badge.fury.io/py/repo2txt)

## 🎯 Overview

`repo2txt` is a powerful Python tool designed to streamline the process of preparing codebases for AI training data and LLM interactions. Whether you're feeding code to GPT models, creating documentation, or analyzing project structures, this tool compiles your entire repository into a single, comprehensive document with intelligent filtering and professional formatting.

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
- **Pattern Matching**: Include only specific file types with wildcards
- **Settings Control**: Toggle inclusion of config files
- **Scope Limiting**: Process only specific directories

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
# Via pip (recommended)
pip install repo2txt

# Or clone and run locally
git clone https://github.com/yourusername/repo2txt.git
cd repo2txt
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
   • --include-dir: Process only this directory (excludes all others, then applies file filters like --include-files "*.py")
   • --exclude-dir: Remove these directories (keeps everything else, combines with any flags like --ignore-types .log)
      ↓
3. ✅ File Whitelist Flags (optional - overrides defaults)
   • --include-files: ONLY process files matching these patterns (works within directory scope set by step 2's --include-dir/--exclude-dir, excludes all others). This means we can filter purely by pattern, limit to a directory then filter by pattern, or exclude directories then filter by pattern.
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
| **`--include-dir`** | Limits scope to one directory | ❌ No |
| **`--include-files`** | Whitelist mode - ONLY these files | ⚠️ Overrides ignore-types defaults |
| **Directory filters** | Remove/keep entire directories | ✅ Use `none` to disable |
| **File filters** | Remove individual files | ✅ Use `none` to disable |

### **Filter Interactions**
- 🎯 **Include takes precedence**: `--include-files` overrides `--ignore-types` defaults
- 🔄 **Combines logically**: `--include-files "*.py" --exclude-dir tests` = "Python files but not in test directories"
- 🛡️ **Security first**: `.env` files are always excluded regardless of other settings
- 💡 **Use `none`**: Disable specific filters with `--ignore-types none` or `--exclude-dir none`

## 📋 Usage Patterns

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
repo2txt --include-dir src -o src_all.txt

# Python files in src/ directory only
repo2txt --include-dir src --include-files "*.py" -o src_python.txt

# Everything in src/ except test subdirectories
repo2txt --include-dir src --exclude-dir tests -o src_no_tests.txt
```

### **Blacklist Approach (Everything Except...)**
```bash
# Everything except images/videos (uses default excludes + custom)
repo2txt --ignore-types .jpg .png .mp4 -o no_media.txt

# Everything except test directories
repo2txt --exclude-dir tests __tests__ test -o no_tests.txt

# All file types but skip settings files
repo2txt --ignore-types none --ignore-settings -o code_only.txt
```

### **Mixed Strategies**
```bash
# Python/JS files, but skip test directories
repo2txt --include-files "*.py" "*.js" --exclude-dir tests -o code_no_tests.txt

# Everything in backend/ except logs and temp files
repo2txt --include-dir backend --ignore-files "*.log" "*.tmp" -o backend_clean.txt

# Config files but not from node_modules
repo2txt --include-files "*.json" "*.yaml" --exclude-dir node_modules -o clean_configs.txt
```

### **Debugging & Analysis**
```bash
# See what would be processed without generating output
repo2txt --dry-run --verbose

# Check specific directory structure
repo2txt --include-dir src --dry-run --verbose

# Test file patterns
repo2txt --include-files "*.py" --dry-run
```

## ⚙️ Configuration

### **Command-Line Reference**

| Flag | Behavior | Example |
|------|----------|---------|
| `-r PATH` | Repository path | `-r /path/to/repo` |
| `-o FILE` | Output file (.txt/.docx) | `-o docs.docx` |
| `--include-dir DIR` | **Scope to directory only** | `--include-dir src` |
| `--include-files PATTERNS` | **Whitelist: ONLY these files** | `--include-files "*.py" "*.js"` |
| `--exclude-dir DIRS` | Remove directories | `--exclude-dir tests docs` |
| `--ignore-files FILES` | Skip specific files | `--ignore-files README.md` |
| `--ignore-types EXTS` | Skip file extensions | `--ignore-types .log .tmp` |
| `--ignore-settings` | Skip config files | `--ignore-settings` |
| `--verbose` | Show processing details | `--verbose` |
| `--dry-run` | Preview only (no output) | `--dry-run` |

**Use `none` to disable**: `--ignore-types none`, `--exclude-dir none`

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
│   └── tests/
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

# Language-specific
repo2txt --include-files "*.py"             # Python only
repo2txt --include-files "*.py" "*.js"      # Python + JavaScript

# Directory-focused  
repo2txt --include-dir src                  # Only src/ directory
repo2txt --include-dir api --include-files "*.py"  # Python files in api/ only

# Clean output (no build artifacts)
repo2txt --exclude-dir node_modules dist build     # Skip common build dirs
repo2txt --ignore-types none --exclude-dir tests   # All files except tests

# Configuration files
repo2txt --include-files "*.json" "*.yaml" "*.toml"  # Config files only

# Debugging
repo2txt --dry-run --verbose               # See what would be processed
```

## 🤝 Use Cases

### 🤖 **AI/ML Training Data**
Perfect for creating clean, structured datasets for training code-aware AI models:

```bash
# Clean Python training data
repo2txt --include-files "*.py" --exclude-dir tests __pycache__ -o python_training.txt

# Multi-language dataset
repo2txt --include-files "*.py" "*.js" "*.java" "*.cpp" -o multilang_training.txt
```

### 📚 **Documentation Generation**
Generate comprehensive project documentation:

```bash
# Full project overview
repo2txt --exclude-dir node_modules .git -o project_overview.docx

# Developer onboarding docs
repo2txt --include-dir src docs --ignore-types .pyc .log -o onboarding.txt
```

### 🔍 **Code Analysis**
Analyze codebases for patterns and structure:

```bash
# Security audit preparation
repo2txt --include-files "*.py" "*.js" "*.php" -o security_audit.txt

# Architecture review
repo2txt --include-dir src --exclude-dir tests -o architecture_review.docx
```

## 🐛 Troubleshooting

| Issue | Solution | Command |
|-------|----------|---------|
| **Files missing from output** | Use verbose to see what's excluded | `repo2txt --verbose --dry-run` |
| **Permission denied errors** | Check which directories are inaccessible | `repo2txt --verbose` |
| **Too many files** | Use whitelist approach | `--include-files "*.py" "*.js"` |
| **Wrong directory scope** | Verify include-dir path | `--include-dir src --dry-run` |
| **Unexpected file types** | Check default ignore list | `--ignore-types none --verbose` |

### **Understanding Output**
- **Verbose shows**: Which files are processed, permission errors, file counts
- **Dry-run shows**: What would be included without generating output
- **File paths**: Relative to repo root (or include-dir if specified)

## 🔄 Version History

### v2.0.0 (Latest)
- ✨ Added `--include-files` pattern matching
- 🛡️ Enhanced error handling and encoding support
- 📊 Added verbose mode and dry-run functionality
- 🎨 Improved DOCX formatting with monospace fonts
- ⚡ Better performance for large repositories
- 🔧 Comprehensive configuration options

### v1.x.x
- 📄 Basic text and DOCX output
- 🌳 Directory tree generation
- 🚫 Basic file filtering

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 **Bug Reports**
- Use the issue tracker with detailed reproduction steps
- Include sample repository structure if possible
- Provide verbose output logs

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