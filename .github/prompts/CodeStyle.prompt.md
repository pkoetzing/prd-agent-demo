# Python Code Style and Best Practices

## PEP 8 Compliance
- Adhere to the PEP 8 style guide for Python code.
- Limit line length to:
  - **79 characters** for code.
  - **72 characters** for comments and docstrings.
- Use hanging indentation only for line continuations; avoid placing a single closing brace, bracket, or parenthesis on a separate line.
- Use:
  - **Single quotes** for strings.
  - **Double quotes** for docstrings.
- Include type hints for all functions and methods.
- Add docstrings for all functions and methods, ensuring they do not repeat the function signature.

## Linting and Formatting
- Use `ruff` for linting and formatting.
- Ensure that all code passes `ruff` checks.
- Use Google-style docstrings for all functions and classes.
- Add type hints for all functions and methods.

## Logging Guidelines
- Use the `logging` module for all logging purposes.
- Configure logging to:
  - Write **info messages** to the console.
  - Write **debug messages** to a file.
- Use the following logging format and date format:
  - `format='%(asctime)s:%(levelname)s:%(message)s'`
  - `datefmt='%Y-%m-%d %H:%M:%S'`

## Pandas Best Practices
- When working with timeseries data always convert the timestamp
  column to a DatetimeIndex and use it as the DataFrame’s index;
  do not leave timestamps in a separate column or separate list
  and do not separate timestamps from the values
- Avoid using `inplace=True` with pandas operations.
- Prefer method chaining for cleaner and more readable pandas code.

## File Handling
- Use the `pathlib` module for file and directory operations.

## Security

- All code must be checked for common security vulnerabilities (e.g., injection, unsafe file handling, insecure deserialization, use of eval/exec, hardcoded secrets).
- Use secure coding practices: validate all inputs, sanitize data, avoid insecure functions, and handle sensitive data
