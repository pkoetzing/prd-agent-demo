## Virtual Environment (VENV)

- Create a requirements file named `requirements.txt` in the root directory
  and add the following default packages:
  - `pandas`
  - `pandas-stubs`
  - `numpy`
  - `pyarrow`
  - `pytest`
  - `python-dotenv`
  - `ipykernel`
  - `ruff`
  - `mypy`
- Add additional packages as needed for the project.
- Create a separate vitual environment via `python -m venv .venv`
- Install the current project in the `.venv`
  in editable mode using `pip install -e .`
- Document the virtual environment setup in the `README.md` file.
- Ensure the virtual environment is activated
  before running any scripts or tests.