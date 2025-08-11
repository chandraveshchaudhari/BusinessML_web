import os
import shutil
import subprocess
from pathlib import Path

# --- CONFIG ---
NOTEBOOKS_DIR = Path("notebooks")
DOCS_DIR = Path("docs")
TEMP_NOTEBOOKS_DIR = Path("temp_notebooks")
JUPYTERLITE_BUILD_DIR = Path("jupyterlite_build")
JUPYTERLITE_OUTPUT_DIR = DOCS_DIR / "jupyterlite"
FORCE_BUTTON_SCRIPT = Path("forced_jupyterlite_button.py")

def run_cmd(cmd, cwd=None):
    """Run a shell command with live output."""
    print(f"\n[RUNNING] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")

def clean_dir(path):
    """Delete a folder if it exists."""
    if path.exists():
        print(f"[CLEANING] {path}")
        shutil.rmtree(path)

def build_jupyterbook():
    """Step 1: Build JupyterBook from notebooks and move HTML to docs/."""
    print("\n=== Building JupyterBook ===")
    run_cmd(["jupyter-book", "build", NOTEBOOKS_DIR])

    html_build_path = NOTEBOOKS_DIR / "_build" / "html"

    if not html_build_path.exists():
        raise FileNotFoundError(f"JupyterBook HTML build not found at {html_build_path}")

    # Clean old docs (except jupyterlite folder if exists)
    if DOCS_DIR.exists():
        for item in DOCS_DIR.iterdir():
            if item.is_dir() and item.name == "jupyterlite":
                continue
            if item.is_file() or item.is_dir():
                shutil.rmtree(item) if item.is_dir() else item.unlink()

    # Move new HTML files into docs/
    for item in html_build_path.iterdir():
        dest = DOCS_DIR / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
    print("[DONE] JupyterBook build copied to docs/")

def build_jupyterlite():
    """Step 2: Prepare notebooks, build JupyterLite, patch HTML, and move output."""
    print("\n=== Building JupyterLite ===")
    clean_dir(TEMP_NOTEBOOKS_DIR)
    TEMP_NOTEBOOKS_DIR.mkdir()

    # Copy notebooks to temp
    for nb in NOTEBOOKS_DIR.glob("*.ipynb"):
        shutil.copy2(nb, TEMP_NOTEBOOKS_DIR / nb.name)

    # Build JupyterLite
    clean_dir(JUPYTERLITE_BUILD_DIR)
    run_cmd(["jupyter", "lite", "build", "--contents", str(TEMP_NOTEBOOKS_DIR), "--output-dir", str(JUPYTERLITE_BUILD_DIR)])

    # Run forced_jupyterlite_button.py
    if FORCE_BUTTON_SCRIPT.exists():
        run_cmd(["python", str(FORCE_BUTTON_SCRIPT)])
    else:
        print("[WARNING] forced_jupyterlite_button.py not found. Skipping patch.")

    # Move JupyterLite output to docs/jupyterlite
    clean_dir(JUPYTERLITE_OUTPUT_DIR)
    shutil.copytree(JUPYTERLITE_BUILD_DIR, JUPYTERLITE_OUTPUT_DIR)
    print("[DONE] JupyterLite build copied to docs/jupyterlite")

    # Clean temp
    clean_dir(TEMP_NOTEBOOKS_DIR)
    clean_dir(JUPYTERLITE_BUILD_DIR)

if __name__ == "__main__":
    build_jupyterbook()
    build_jupyterlite()
    print("\n✅ All steps completed successfully!")
