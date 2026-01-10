# Testing Instructions

## Running Tests in a Fresh Environment

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Setup Steps

1. **Create a Virtual Environment**

   ```bash
   python -m venv .venv
   ```

2. **Activate the Virtual Environment**

   On Windows (PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   On Windows (Command Prompt):

   ```cmd
   .venv\Scripts\activate.bat
   ```

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

3. **Install the Package in Development Mode**

   ```bash
   pip install -e .
   ```

4. **Run the Tests**

   ```bash
   python -m unittest discover -s tests -p "test_*.py"
   ```

   Or run a specific test file:

   ```bash
   python tests/test_vessel.py
   ```

### Expected Output

All tests should pass with output similar to:

```
.....
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

### What Each Test Does

- `test_velocity_north`: Verifies velocity calculation for northward heading (0°)
- `test_velocity_east`: Verifies velocity calculation for eastward heading (90°)
- `test_velocity_south`: Verifies velocity calculation for southward heading (180°)
- `test_velocity_west`: Verifies velocity calculation for westward heading (270°)
- `test_velocity_diagonal`: Verifies velocity calculation for diagonal heading (45°)

### Troubleshooting

**Issue: ModuleNotFoundError**

- Ensure you've installed the package with `pip install -e .`
- Verify the virtual environment is activated

**Issue: Python version mismatch**

- Ensure you're using Python 3.9+
- Check with: `python --version`

**Issue: Tests fail with different expected values**

- The tests use `assertAlmostEqual` with 6 decimal places precision
- This accounts for floating-point rounding errors in trigonometric calculations
