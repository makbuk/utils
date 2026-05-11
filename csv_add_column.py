"""
csv_add_column.py — add a new column to a CSV file.

The delimiter is detected automatically.
The new column can be placed at the beginning or end of each row.
Its value is either a fixed string or empty (default).

Usage:
    python csv_add_column.py data.csv --name status
    python csv_add_column.py data.csv --name status --value pending
    python csv_add_column.py data.csv --name tag --value new --position start
    python csv_add_column.py data.csv --name note --output result.csv
"""

import argparse
import csv
import sys
from pathlib import Path


def detect_delimiter(path: Path) -> str:
    """Sniff the delimiter from the first 4 KB of the file."""
    try:
        sample = path.read_bytes()[:4096].decode("utf-8-sig", errors="replace")
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        return dialect.delimiter
    except csv.Error:
        return ","  # safe default


def add_column(
    src: Path,
    dst: Path,
    col_name: str,
    col_value: str,
    position: str,          # "start" | "end"
) -> int:
    """
    Read src CSV, add a column, write to dst.
    Returns the number of data rows written.
    """
    delimiter = detect_delimiter(src)
    delim_name = repr(delimiter)
    print(f"  Detected delimiter : {delim_name}")
    print(f"  Column name        : {col_name!r}")
    print(f"  Column value       : {col_value!r}")
    print(f"  Position           : {position}")

    rows_written = 0

    with (
        src.open(newline="", encoding="utf-8-sig") as fin,
        dst.open("w", newline="", encoding="utf-8")  as fout,
    ):
        reader = csv.reader(fin, delimiter=delimiter)
        writer = csv.writer(fout, delimiter=delimiter)

        for i, row in enumerate(reader):
            if i == 0:
                # Header row
                new_header = [col_name] + row if position == "start" else row + [col_name]
                writer.writerow(new_header)
            else:
                new_row = [col_value] + row if position == "start" else row + [col_value]
                writer.writerow(new_row)
                rows_written += 1

    return rows_written


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add a column to a CSV file (delimiter auto-detected)"
    )
    parser.add_argument("csv_file",  metavar="CSV",   help="Input CSV file")
    parser.add_argument("--name",    required=True,   help="New column name (header)")
    parser.add_argument("--value",   default="",      help="Value for every row (default: empty)")
    parser.add_argument("--position", choices=["start", "end"], default="end",
                        help="Where to insert the column: start or end (default: end)")
    parser.add_argument("--output",  "-o", metavar="FILE",
                        help="Output file (default: overwrite input file)")
    args = parser.parse_args()

    src = Path(args.csv_file)
    if not src.exists():
        print(f"[ERROR] File not found: {src}")
        sys.exit(1)

    dst = Path(args.output) if args.output else src

    # Write to a temp file first to avoid corrupting src when dst == src
    tmp = src.with_suffix(".tmp.csv")
    try:
        rows = add_column(src, tmp, args.name, args.value, args.position)
        tmp.replace(dst)
    except Exception as exc:
        tmp.unlink(missing_ok=True)
        print(f"[ERROR] {exc}")
        sys.exit(1)

    label = "updated" if dst == src else "written"
    print(f"\n[OK] {rows} rows {label} -> {dst.resolve()}")


if __name__ == "__main__":
    main()
