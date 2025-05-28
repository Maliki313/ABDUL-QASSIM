"""
parse_history.py
-----------------

This script loads ChatGPT conversation history exported using the
"Export data" option from your ChatGPT settings. The exported file is a JSON
archive. This script extracts the conversations and saves them in a more
convenient format such as plain text files.

Usage:
    python parse_history.py path_to_export.json output_dir

The export file typically has a structure like::

    {
        "conversations": [
            {
                "title": "My conversation",
                "mapping": { ... }
            },
            ...
        ]
    }

The `mapping` field contains the messages. This script walks the mapping
and writes each conversation to ``output_dir/<title>.txt``.

You need Python 3.8+.
"""
import json
import sys
from pathlib import Path

def extract_text_from_mapping(mapping):
    """Yield message texts in order from a conversation mapping."""
    # Each mapping entry is keyed by message ID with info about parent
    # relationships. We iterate in chronological order using the
    # 'create_time' field.
    items = list(mapping.values())
    items.sort(key=lambda x: x.get('create_time', 0))
    for item in items:
        msg = item.get('message')
        if not msg:
            continue
        content = msg.get('content', {})
        parts = content.get('parts', [])
        for part in parts:
            yield part


def write_conversation(conv, out_dir):
    """Write a single conversation to a text file."""
    title = conv.get('title', 'conversation')
    mapping = conv.get('mapping', {})
    outfile = Path(out_dir) / f"{title}.txt"
    with outfile.open('w', encoding='utf-8') as f:
        for part in extract_text_from_mapping(mapping):
            f.write(part)
            f.write('\n')


def main():
    if len(sys.argv) != 3:
        print('Usage: python parse_history.py export.json output_dir')
        return
    export_file = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(export_file.read_text(encoding='utf-8'))
    for conv in data.get('conversations', []):
        write_conversation(conv, out_dir)
    print(f"Wrote {len(data.get('conversations', []))} conversations to {out_dir}")


if __name__ == '__main__':
    main()
