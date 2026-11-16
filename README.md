# freshcart-pipelines

Data Engineering Assignment - From Git to Gold

## Project layout

- `elt/freshcart.ipynb` contains the FreshCart Snowflake ELT pipeline.
- `iris_project/` contains the Mage Iris classification pipeline.
- `stream/` contains the RabbitMQ dispatcher and driver programs.
- `tests/` contains the automated checks used by CI.

Run the local tests with:

```powershell
python -m pytest
```

Run a stream driver with:

```powershell
python stream/driver.py Ravi "bangalore.koramangala.*"
```

The CI workflow runs the test suite on every push and pull request.