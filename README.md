# CSV cleanup — demonstration

An AI-assisted sample created for Mathew Kriger's small automation service. This is a demonstration, not prior client work.

Requires Python 3. No third-party packages, network access, or paid services.

Run:

    python clean_csv.py example.csv result.csv --key email

It trims surrounding whitespace, drops fully blank records, and keeps the first record for each case-insensitive, nonempty email. Missing email records are retained. Repeat `--key` for composite keys (all must be present to deduplicate). Header names are exact and case-sensitive. All values remain strings, preserving leading zeros. Embedded commas and newlines follow CSV quoting rules. Input is unchanged; an existing output is never overwritten. Malformed column counts are rejected before writing.

Expected sample report: 5 input records, 3 output records, 1 duplicate, 1 blank record.
The included `cleaned.csv` shows the expected output. Use a new output filename on each run; the tool intentionally refuses to overwrite files.

Run the included checks:

    python test_clean_csv.py

Customization can include different duplicate rules, report fields, or export layouts after agreeing a client's scope. This tool does not validate whether an email address exists. Output is CSV data; importing untrusted formula-like values into spreadsheet software requires an appropriate import policy.
