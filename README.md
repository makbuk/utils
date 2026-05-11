# utils

A collection of small command-line utility scripts.

---

## csv_add_column.py

Add a new column to a CSV file. The delimiter is detected automatically.

**Usage**

```
python csv_add_column.py <CSV> --name <col> [--value <val>] [--position start|end] [--output <file>]
```

**Arguments**

| Argument | Required | Default | Description |
|---|---|---|---|
| `CSV` | yes | — | Input CSV file |
| `--name` | yes | — | New column header name |
| `--value` | no | `""` | Value to fill for every data row |
| `--position` | no | `end` | Insert column at `start` or `end` |
| `--output`, `-o` | no | overwrite input | Output file path |

**Examples**

```bash
# Add empty "status" column at the end
python csv_add_column.py data.csv --name status

# Add "status" column pre-filled with "pending"
python csv_add_column.py data.csv --name status --value pending

# Insert "tag" column at the start
python csv_add_column.py data.csv --name tag --value new --position start

# Write to a separate output file
python csv_add_column.py data.csv --name note --output result.csv
```
