"""تفاصيل السكربت
------------------

هذا السكربت يقرأ أرشيف محادثات ChatGPT اللي تصدره من الإعدادات عبر خيار
"Export data". الملف المصدَّر يكون بصيغة JSON ونحوّله إلى ملفات نصية عادية
حتى تستخدمها أو تدرب نماذجك بلا إنترنت.

طريقة الاستخدام:

```
python parse_history.py path_to_export.json output_dir
```

عادةً هيكلية الملف تكون بهذا الشكل::

    {
        "conversations": [
            {
                "title": "مثال محادثة",
                "mapping": { ... }
            },
            ...
        ]
    }

الحقل ``mapping`` يحتوي الرسائل. السكربت يمشي على هالهيكل ويكتب كل محادثة
داخل ``output_dir/<title>.txt``.

ملاحظة: يحتاج بايثون 3.8 أو أحدث.
"""
import json
import sys
from pathlib import Path
import re


def slugify(name):
    """تحويل العنوان إلى اسم ملف آمن.

    **المدخلات**:
        - ``name`` (:class:`str`): العنوان الأصلي.

    **المخرجات**:
        - الاسم بعد إزالة المحارف غير المناسبة.
    """
    slug = re.sub(r"[^\w-]+", "_", name).strip("_")
    return slug or "conversation"

def extract_text_from_mapping(mapping):
    """استخراج رسائل المحادثة بالترتيب.

    **المدخلات**:
        - ``mapping`` (:class:`dict`): هيكل الرسائل كما يصدره ChatGPT.

    **المخرجات**:
        - يولد نص كل رسالة على حدة.

    **ملاحظات**:
        يمشي على الحقل ``create_time`` حتى يضمن الترتيب الصحيح.
    """
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
    """حفظ محادثة واحدة في ملف نصي.

    **المدخلات**:
        - ``conv`` (:class:`dict`): بيانات المحادثة.
        - ``out_dir`` (:class:`Path`): المسار اللي راح نخزن به الملفات.

    **المخرجات**:
        - لا شيء، لكنه ينشئ ملفاً داخل ``out_dir``.
    """
    title = slugify(conv.get('title', 'conversation'))
    mapping = conv.get('mapping', {})
    outfile = Path(out_dir) / f"{title}.txt"
    with outfile.open('w', encoding='utf-8') as f:
        for part in extract_text_from_mapping(mapping):
            f.write(part)
            f.write('\n')


def main():
    """نقطة تشغيل السكربت."""

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
