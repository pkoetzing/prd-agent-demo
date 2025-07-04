---
mode: 'agent'
tools: [
   'codebase', 'editFiles', 'runCommand',
   'problems', 'runtasks',
   'findTestFiles', 'testFailure',
   'terminalLastCommand', terminalSelection',
   ]
description: 'Generate a new MVP from a product requirement document.'
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

## 6. Documentation
   Create a `README.md` file in the root directory.
   Include instructions for
   - setting up the virtual environment and installing dependencies
   - running the tests
   - running the application

## 7. Virtual Environmen
   Create a virtual environment according to #file:Venv.prompt.md

## 8. Testing
   - Ensure all code passes linting (`ruff`) and type checks (`mypy`).
   - Run all tests and ensure they pass.
   - Execute the `main.py` file and verify it works as expected.
   - Address and resolve any runtime errors encountered.

## 9. Follow Guidelines
   - Refer to #file:ProjectStructure.prompt.md
     for the required directory structure.
   - Use #file:Testing.prompt.md for testing guidelines.
   - Adhere to the coding standards outlined in #file:CodeStyle.prompt.md
