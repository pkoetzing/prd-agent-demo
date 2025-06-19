## Virtual Environment (VENV)

- Create a separate vitual environment using `python -m venv .venv`
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