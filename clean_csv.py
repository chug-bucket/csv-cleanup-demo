"""Standard-library CSV cleanup demo. Input files are never modified."""
import argparse
import csv
import json
from pathlib import Path


def clean(source, target, keys):
    source, target = Path(source), Path(target)
    if source.resolve() == target.resolve():
        raise ValueError('Input and output must be different files')
    if target.exists():
        raise ValueError('Output already exists; choose a new filename')
    with source.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        if not fields or any(not field.strip() for field in fields) or len(set(fields)) != len(fields):
            raise ValueError('A unique, nonempty header is required')
        if any(key not in fields for key in keys):
            raise ValueError('Every key must match a header exactly')
        records, seen = [], set()
        counts = dict(input_rows=0, output_rows=0, duplicates=0, blank_rows=0)
        for line, row in enumerate(reader, start=2):
            counts['input_rows'] += 1
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'Wrong number of columns near record {line}')
            row = {key: value.strip() for key, value in row.items()}
            if not any(row.values()):
                counts['blank_rows'] += 1
                continue
            identity = tuple(row[key].casefold() for key in keys)
            # Missing keys never cause unrelated records to collapse.
            can_dedupe = all(row[key] for key in keys)
            if can_dedupe and identity in seen:
                counts['duplicates'] += 1
                continue
            if can_dedupe:
                seen.add(identity)
            records.append(row)
        counts['output_rows'] = len(records)
    # Validate every record before creating the output.
    with target.open('x', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
    return counts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--key', action='append', required=True,
                        help='Deduplication header; repeat for a composite key')
    args = parser.parse_args()
    try:
        print(json.dumps(clean(args.input, args.output, args.key), indent=2))
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(1, f'Error: {error}\n')
