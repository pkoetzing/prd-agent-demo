---
mode: 'agent'
tools: ['promptBoost', 'codebase']
description: 'Generate a new MVP from a product requirement document.'
---
PRD to use: #file:../../docs/rwy-finder-prd.md

1. **Complete the MVP**: Implement the full Minimum Viable Product (MVP) without waiting for feedback or seeking clarification. Make reasonable assumptions where necessary.
2. **Autonomous Changes**: Make any changes you deem necessary without asking for permission. Document all changes in a `changelog.md` file located in the `docs` directory.
3. **Documentation**:
   - Create a `README.md` file in the root directory. Include instructions on how to use the code and run the tests.
4. **Testing**:
   - Run all tests and ensure they pass.
   - Execute the `main.py` file and verify it works as expected. Address and resolve any runtime issues encountered.
5. **Follow Guidelines**:
   - Refer to #file:ProjectStructure.prompt.md for the required directory structure.
   - Use #file:Testing.prompt.md for testing guidelines.
   - Adhere to the coding standards outlined in #file:CodeStyle.prompt.md
