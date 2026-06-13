import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

before = content

# Fix: pd.read_json(data_store['df'], orient='records')
content = content.replace(
    "pd.read_json(data_store['df'], orient='records')",
    "pd.read_json(io.StringIO(data_store['df']), orient='records')"
)
# Fix: pd.read_json(data_store['df'])
content = content.replace(
    "pd.read_json(data_store['df'])",
    "pd.read_json(io.StringIO(data_store['df']))"
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

changes = len(re.findall(r'io\.StringIO', content)) - len(re.findall(r'io\.StringIO', before))
print(f'Done. Fixed {len(re.findall(r"io.StringIO", content))} read_json calls to use io.StringIO.')
