---
mode: 'agent'
tools: [
   'codebase', 'editFiles', 'runCommand',
   'problems', 'runtasks',
   'findTestFiles', 'testFailure',
   'terminalLastCommand', terminalSelection',
   ]
description: 'Create a Minimal Viabale Product (MVP) from a Product Requirement Document (PRD)'
---

# Create a Minimal Viabale Product (MVP) from a Product Requirement Document (PRD)

PRD to use: #file:../../docs/rwy-finder-prd.md

## 1. Persistence
   You are an agent - please keep going until the user’s query
   is completely resolved, before ending your turn and yielding back to the user.
   Only terminate your turn when you are sure that the problem is solved.

## 2. Tool-calling
   If you are not sure about file content or codebase structure
   pertaining to the user’s request, use your tools to read files
   and gather the relevant information: do NOT guess or make up an answer.

## 3. Planning
   You MUST plan extensively before each function call, and reflect extensively
   on the outcomes of the previous function calls. DO NOT do this entire process
   by making function calls only, as this can impair your ability to solve
   the problem and think insightfully.

## 4. Complete the MVP
   Implement the full Minimum Viable Product (MVP)
   without waiting for feedback or seeking clarification.
   Make reasonable assumptions where necessary.

## 5. Autonomous Changes
   Make any changes you deem necessary without asking for permission.
   Document all changes in a `changelog.md` file
   located in the `docs` directory.

## 6. Projet Folder Structure
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

## 6. Documentation
   Create a `README.md` file in the root directory.
   Include instructions for
   - setting up the virtual environment and installing dependencies
   - running the tests
   - running the application

## 7. Virtual Environmen
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

## 8. Linting
   - Ensure all code passes linting (`ruff`) and type checks (`mypy`).

## 9. Testing
   - Use the `pytest` module to write unit tests.
   - Place all unit test files in the `tests/` directory.
   - Avoid using mocking; focus on testing actual functionality.
   - Execute all tests using `pytest` and resolve any errors or failures encountered.
   - Aim for at least 80% code coverage in unit tests.
   - Document how to run tests in the `README.md`.

## 10. Debugging
   - Execute the `main.py` file and verify it works as expected.
   - Address and resolve any runtime errors encountered.
