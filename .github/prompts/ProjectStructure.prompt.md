## Directory Structure

- keep all scripts and notebooks (if any) in the main directory unless otherwise specified.
- Adhere to the following structure:
  - `.` (main script)
  - `<package_name>/` (package code)
  - `tests/` (unit tests)
  - `docs/` (documentation)
    - `docs/changelog.md` (changelog)
  - `.venv/` (virtual environment)
  - `requirements.txt` (dependencies)
  - `.gitignore` (Git ignore file)
    - Add `data/` to `.gitignore`
  - `.env` (environment variables)
    - Use `dotenv` to load environment variables from `.env`
    - Add `DATA_Path=data` to `.env`
  - Use a `pyproject.toml` file for project metadata.
  - The `pyproject.toml` file must include project metadata such as name, version, and dependencies.
  
## Virtual Environment (VENV)

- Always create a separate `.venv` directory for each project.
- Use a `requirements.txt` file to manage dependencies.
- Install the following packages in the `.venv`:
  - `pandas`
  - `pandas-stubs`
  - `numpy`
  - `pyarrow`
  - `pytest`
  - `python-dotenv`
  - `ipykernel`
  - `ruff`
  - `mypy`
- Install the current package in the `.venv` in editable mode using `pip install -e .`.