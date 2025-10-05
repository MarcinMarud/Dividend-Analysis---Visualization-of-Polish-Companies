import subprocess
import sys
import os


def run_script(script_path):
    print(f"--- Running {script_path} ---")
    try:
        process = subprocess.run(
            [sys.executable, script_path], check=True, capture_output=True, text=True)
        print(f"Successfully ran {script_path}")
        if process.stderr:
            print("Errors/Warnings (may be harmless):\n", process.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}:")
        print("Stdout:\n", e.stdout)
        print("Stderr:\n", e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(
            f"Error: Script file '{script_path}' not found at the specified path.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while running {script_path}: {e}")
        sys.exit(1)
    print("-" * (len(script_path) + 12))


if __name__ == "__main__":
    run_script(os.path.join("src", "data", "data_scraping.py"))
    run_script(os.path.join("sql", "database_management", "database_insert.py"))
    run_script(os.path.join("sql", "database_management", "creating_views.py"))

    print("All scripts executed successfully.")
