import subprocess
from pathlib import Path

def run_repo2txt(args, output_file):
    output_path = Path(output_file)
    if output_path.exists():
        output_path.unlink()
    subprocess.run(
        ["python", "src/repo2txt/repo2txt.py", *args, "-o", output_file],
        check=True
    )
    return output_path.read_text()

def test_exclude_ios(tmp_path):
    output = run_repo2txt(["--include-dir", "test-repo", "--exclude-dir", "ios"], tmp_path / "out1.txt")
    assert "ios/" not in output
    assert "helper.swift" not in output
    assert "AppDelegate.swift" not in output
    assert "README.md" in output
    assert "utils.py" in output

def test_include_only_nested_ios(tmp_path):
    output = run_repo2txt(["--include-dir", "test-repo/src/ios"], tmp_path / "out2.txt")
    assert "helper.swift" in output
    assert "AppDelegate.swift" not in output
    assert "README.md" not in output

def test_include_py_files_only(tmp_path):
    output = run_repo2txt(["--include-dir", "test-repo", "--include-files", "*.py"], tmp_path / "out3.txt")
    assert "utils.py" in output
    assert "MainActivity.kt" not in output
    assert "AppDelegate.swift" not in output
    assert "helper.swift" not in output
    # folders may appear even if their files are excluded
    assert "android" in output
    assert "ios" in output
