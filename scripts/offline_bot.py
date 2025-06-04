"""
offline_bot.py
---------------

هالسكربت يقرأ ملفات النصوص عندك حتى يجاوب على سؤالك بلا اتصال بالإنترنت.
يجمع كل الملفات ``.txt`` من مجلد تحدده ويسوي بحث بسيط بالكلمات المفتاحية حتى
يجيب لك أكثر الجمل ارتباطاً بسؤالك.

البرنامج مو نموذج لغوي كامل، بس يعتمد على بحث بسيط. تقدر تطوره وتربطه بنموذج
مفتوح المصدر أو مكتبة تعالج التضمين مثل `sentence-transformers`.

طريقة الاستخدام::

    python offline_bot.py data_dir "your question here"

"""
import sys
from pathlib import Path
import re


def load_sentences(data_dir):
    """ 
    تجمع الجمل من كل ملفات ``.txt`` داخل المجلد المحدد.

    المدخلات:
        data_dir (str | Path): مسار المجلد اللي يحتوي الملفات.

    المخرجات:
        list[tuple[str, str]]: قائمة بالجمل مع اسم الملف.
    """
    sentences = []
    for path in Path(data_dir).rglob('*.txt'):
        text = path.read_text(encoding='utf-8')
        for line in text.splitlines():
            line = line.strip()
            if line:
                sentences.append((path.name, line))
    return sentences


def simple_search(sentences, query):
    """
    تبحث عن الجمل اللي تحتوي كل كلمات السؤال.

    المدخلات:
        sentences (list[tuple[str, str]]): الجمل مع اسم الملف.
        query (str): السؤال المطلوب البحث عنه.

    المخرجات:
        list[tuple[str, str]]: الجمل المطابقة.
    """
    keywords = re.findall(r"\w+", query.lower())
    results = []
    for name, sentence in sentences:
        s_lower = sentence.lower()
        if all(word in s_lower for word in keywords):
            results.append((name, sentence))
    return results


def main():
    if len(sys.argv) < 3:
        print('Usage: python offline_bot.py data_dir "question"')
        return
    data_dir = sys.argv[1]
    query = ' '.join(sys.argv[2:])
    sentences = load_sentences(data_dir)
    results = simple_search(sentences, query)
    if not results:
        print('No results found.')
    else:
        for name, sentence in results[:5]:
            print(f'[{name}] {sentence}')


if __name__ == '__main__':
    main()
