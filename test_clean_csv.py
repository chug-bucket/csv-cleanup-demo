import csv
import importlib.util
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('demo', root / 'clean_csv.py')
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)
with tempfile.TemporaryDirectory() as folder:
    source, output = Path(folder)/'in.csv', Path(folder)/'out.csv'
    source.write_text('email,zip,notes\na@b.test,00123,"two\nlines"\nA@B.TEST,00123,duplicate\n,00456,one\n,00789,two\n', encoding='utf-8', newline='')
    original = source.read_bytes()
    result = demo.clean(source, output, ['email'])
    rows = list(csv.DictReader(output.open(newline='', encoding='utf-8')))
    assert result['output_rows'] == 3 and result['duplicates'] == 1
    assert rows[0]['zip'] == '00123' and rows[0]['notes'] == 'two\nlines'
    assert source.read_bytes() == original
    try:
        demo.clean(source, output, ['email'])
        raise AssertionError('Existing output overwritten')
    except ValueError:
        pass
    source.write_text('email,zip\na@b.test,00123,extra\n', encoding='utf-8')
    malformed_output = Path(folder)/'invalid.csv'
    try:
        demo.clean(source, malformed_output, ['email'])
        raise AssertionError('Malformed record accepted')
    except ValueError:
        assert not malformed_output.exists()
    source.write_text('email,\na@b.test,value\n', encoding='utf-8')
    empty_header_output = Path(folder)/'empty-header.csv'
    try:
        demo.clean(source, empty_header_output, ['email'])
        raise AssertionError('Blank column name accepted')
    except ValueError:
        assert not empty_header_output.exists()
print('Passed: identifiers, quoted newlines, deduplication, missing keys, input preservation, overwrite protection, malformed records')

