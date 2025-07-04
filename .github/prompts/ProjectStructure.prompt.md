## Directory Structure

- Keep all scripts and notebooks (if any) in the main directory
  unless otherwise specified.
- Adhere to the following structure:
  - `.` (main script)
  - `<package_name>/` (package code)
  - `tests/` (unit tests)
  - `docs/` (documentation)
    - `docs/changelog.md` (changelog)
  - `requirements.txt` (dependencies)
  - `.gitignore` (Git ignore file)
    - Add `.venv` to `.gitignore`
  - `.env` (environment variables)
    - Use `dotenv` to load environment variables from `.env`
    - Add `DATA_Path=data` to `.env`
  - Use a `pyproject.toml` file for project metadata.
  - The `pyproject.toml` file must include project metadata such as name,
    version, and dependencies.

