"""
parse_history.py
-----------------

الملف هذا يقرأ سجل محادثات ChatGPT اللي تصدره من خيار "تصدير البيانات".
يكون الملف بصيغة JSON ونسحب منه المحادثات ونحولها لملفات نصية أخف.

طريقة الاستخدام:
    python parse_history.py path_to_export.json output_dir

عادةً الملف المصدر يكون بهالشكل::

    {
        "conversations": [
            {
                "title": "My conversation",
                "mapping": { ... }
            },
            ...
        ]
    }

حقل ``mapping`` يحتوي الرسائل، نمشي عليه ونكتب كل محادثة في
``output_dir/<title>.txt``.

يحتاج السكربت بايثون 3.8 فما فوق.
"""
import json
import sys
from pathlib import Path
import re


def sanitize_filename(name):
    """
    ينظف العنوان حتى يصير اسم ملف صالح.

    المدخلات:
        name (str): العنوان الأصلي.

    المخرجات:
        str: اسم ملف آمن.
    """
    return re.sub(r"[^\w-]", "_", name)

def extract_text_from_mapping(mapping):
    """
    ترجع نصوص الرسائل بترتيبها الزمني.

    المدخلات:
        mapping (dict): خريطة المحادثة.

    المخرجات:
        Iterable[str]: النصوص بالتسلسل.
    """
    # نرتب الرسائل حسب حقل create_time حتى نحافظ على التسلسل.
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
    """
    تكتب محادثة وحدة في ملف نصي.

    المدخلات:
        conv (dict): بيانات المحادثة.
        out_dir (Path | str): مجلد الإخراج.

    المخرجات:
        None
    """
    title = conv.get('title', 'conversation')
    title = sanitize_filename(title)
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
