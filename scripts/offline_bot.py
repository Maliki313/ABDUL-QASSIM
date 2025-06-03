"""بوت بسيط للعمل بدون إنترنت
------------------------------

هالسكريبت يقرأ ملفات ``.txt`` اللي تحطها داخل مجلد محدد ويجاوب على أسئلتك
باستخدام مطابقة كلمات مفتاحية فقط، من غير ما يعتمد على أي بحث بالويب.

هو مو نموذج لغوي متكامل، بس تقدر تطوره وتدمج مكتبات مثل
`sentence-transformers` لو حبيت.

طريقة الاستخدام:

```
python offline_bot.py notes_dir history_dir "سؤالك هنا"
```
"""
import sys
from pathlib import Path
import re


def load_sentences(data_dirs):
    """قراءة الجمل من مجلد أو أكثر يحتوي ملفات ``.txt``.

    **المدخلات**:
        - ``data_dirs`` (:class:`str` أو :class:`Path` أو ``list``): مسارات المجلدات.

    **المخرجات**:
        - قائمة من ``(اسم_الملف, الجملة)``.
    """
    if isinstance(data_dirs, (str, Path)):
        dirs = [data_dirs]
    else:
        dirs = list(data_dirs)

    sentences = []
    for d in dirs:
        for path in Path(d).rglob('*.txt'):
            text = path.read_text(encoding='utf-8')
            for line in text.splitlines():
                line = line.strip()
                if line:
                    sentences.append((path.name, line))
    return sentences


def simple_search(sentences, query):
    """بحث بسيط يطابق كل الكلمات المفتاحية.

    **المدخلات**:
        - ``sentences`` (:class:`list`): قائمة الجمل من ``load_sentences``.
        - ``query`` (:class:`str`): سؤال المستخدم.

    **المخرجات**:
        - قائمة الجمل المطابقة.
    """
    keywords = re.findall(r"\w+", query.lower())
    results = []
    for name, sentence in sentences:
        s_lower = sentence.lower()
        if all(word in s_lower for word in keywords):
            results.append((name, sentence))
    return results


def main():
    """نقطة تشغيل السكربت."""

    if len(sys.argv) < 3:
        print('Usage: python offline_bot.py data_dir... "question"')
        return
    dirs = sys.argv[1:-1]
    query = sys.argv[-1]
    sentences = load_sentences(dirs)
    results = simple_search(sentences, query)
    if not results:
        print('No results found.')
    else:
        for name, sentence in results[:5]:
            print(f'[{name}] {sentence}')


if __name__ == '__main__':
    main()
