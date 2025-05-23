#!/usr/bin/env python3

import os
import argparse
import json
import fnmatch
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE_PATH = os.path.join(SCRIPT_DIR, 'config.json')

def load_config(file_path=CONFIG_FILE_PATH):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "image_extensions": [], "video_extensions": [], "audio_extensions": [],
            "document_extensions": [], "executable_extensions": [],
            "settings_extensions": [], "additional_ignore_types": [],
            "default_output_file": "output.txt"
        }

config = load_config()
IMAGE_EXTENSIONS = config.get("image_extensions", [])
VIDEO_EXTENSIONS = config.get("video_extensions", [])
AUDIO_EXTENSIONS = config.get("audio_extensions", [])
DOCUMENT_EXTENSIONS = config.get("document_extensions", [])
EXECUTABLE_EXTENSIONS = config.get("executable_extensions", [])
SETTINGS_EXTENSIONS = config.get("settings_extensions", [])
ADDITIONAL_IGNORE_TYPES = config.get("additional_ignore_types", [])
DEFAULT_OUTPUT_FILE = config.get("default_output_file", "output.txt")

DEFAULT_IGNORE_TYPES_LIST = list(set(
    IMAGE_EXTENSIONS + VIDEO_EXTENSIONS + AUDIO_EXTENSIONS +
    DOCUMENT_EXTENSIONS + EXECUTABLE_EXTENSIONS + ADDITIONAL_IGNORE_TYPES
))

def parse_args():
    parser = argparse.ArgumentParser(
        description='Document the structure of a GitHub repository.',
        epilog='To ignore no types: --ignore-types. To include only *.py: --include-files *.py',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-r', '--repo_path', default=os.getcwd())
    parser.add_argument('-o', '--output_file', default=DEFAULT_OUTPUT_FILE)
    parser.add_argument('--ignore-files', nargs='*', default=[])
    parser.add_argument('--ignore-types', nargs='*', default=DEFAULT_IGNORE_TYPES_LIST)
    parser.add_argument('--exclude-dir', nargs='*', default=[])
    parser.add_argument('--ignore-settings', action='store_true')
    parser.add_argument('--include-dir', nargs='?', default=None)
    parser.add_argument('--include-files', nargs='*', default=None)
    return parser.parse_args()

def should_ignore(item_path, args, repo_root_path):
    item_name = os.path.basename(item_path)
    file_ext = os.path.splitext(item_name)[1].lower()

    if os.path.abspath(item_path) == os.path.abspath(args.output_file):
        return True
    if item_name in ['.git', '.vscode', '.idea', '__pycache__', 'node_modules'] and os.path.isdir(item_path):
        return True
    if item_name.startswith('.') and item_path != repo_root_path:
        return True
    if os.path.isdir(item_path) and args.exclude_dir and item_name in args.exclude_dir:
        return True

    if args.include_dir:
        abs_include_dir = os.path.abspath(args.include_dir)
        if not item_path.startswith(abs_include_dir) and not abs_include_dir.startswith(item_path):
            return True

    if os.path.isfile(item_path):
        if args.include_files is not None:
            if not any(fnmatch.fnmatch(item_name, pattern) for pattern in args.include_files):
                return True
        if item_name in args.ignore_files or file_ext in args.ignore_types:
            return True
        if args.ignore_settings and file_ext in SETTINGS_EXTENSIONS:
            return True

    return False

def write_tree(dir_path, output_file, args, repo_root_path, prefix="", is_last=True, is_root=True):
    if is_root:
        output_file.write(f"{os.path.basename(dir_path)}/\n")
    items = sorted(os.listdir(dir_path))
    for idx, item in enumerate(items):
        item_path = os.path.join(dir_path, item)
        if should_ignore(os.path.abspath(item_path), args, repo_root_path):
            continue
        is_last_item = (idx == len(items) - 1)
        output_file.write(f"{prefix}{'└── ' if is_last_item else '├── '}{item}\n")
        if os.path.isdir(item_path):
            write_tree(item_path, output_file, args, repo_root_path,
                       prefix + ('    ' if is_last_item else '│   '), is_last_item, False)

def write_file_content(file_path, output_file, depth):
    indentation = '  ' * depth
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                output_file.write(f"{indentation}{line}")
    except Exception as e:
        output_file.write(f"{indentation}Error reading file: {e}\n")

def write_file_contents_in_order(dir_path, output_file, args, repo_root_path, depth=0):
    items = sorted(os.listdir(dir_path))
    for item in items:
        item_path = os.path.join(dir_path, item)
        if should_ignore(os.path.abspath(item_path), args, repo_root_path):
            continue
        relative_start = os.path.abspath(args.include_dir or args.repo_path)
        relative_path = os.path.relpath(item_path, start=relative_start)
        if os.path.isdir(item_path):
            write_file_contents_in_order(item_path, output_file, args, repo_root_path, depth + 1)
        elif os.path.isfile(item_path):
            output_file.write('  ' * depth + f"[File Begins] {relative_path}\n")
            write_file_content(item_path, output_file, depth)
            output_file.write('  ' * depth + f"[File Ends] {relative_path}\n\n")

def main():
    args = parse_args()
    if args.ignore_files == ['none']: args.ignore_files = []
    if args.exclude_dir == ['none']: args.exclude_dir = []

    processing_root_path = os.path.abspath(args.include_dir or args.repo_path)
    if not os.path.isdir(processing_root_path):
        print(f"Error: {processing_root_path} is not a valid directory.")
        return

    if args.output_file.endswith('.docx'):
        doc = Document()
        doc.styles['Normal'].font.name = 'Arial'
        doc.styles['Normal'].font.size = Pt(10)
        doc.add_heading("Repository Documentation", 1)
        doc.add_heading("Directory/File Tree Begins -->", 2)
        write_tree(processing_root_path, doc, args, processing_root_path)
        doc.add_heading("<-- Directory/File Tree Ends", 2)
        doc.add_heading("File Content Begins -->", 2)
        write_file_contents_in_order(processing_root_path, doc, args, processing_root_path)
        doc.add_heading("<-- File Content Ends", 2)
        doc.save(args.output_file)
    else:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write("Repository Documentation\n\n")
            f.write("Directory/File Tree Begins -->\n\n")
            write_tree(processing_root_path, f, args, processing_root_path)
            f.write("\n<-- Directory/File Tree Ends\n\n")
            f.write("File Content Begins -->\n\n")
            write_file_contents_in_order(processing_root_path, f, args, processing_root_path)
            f.write("\n<-- File Content Ends\n\n")

if __name__ == "__main__":
    main()
