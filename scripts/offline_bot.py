"""
offline_bot.py
---------------

A minimal example of using your own text files to answer questions
without any online search. This script loads all ``.txt`` files from a
specified directory and uses simple keyword matching to return the most
relevant sentences for a query.

This is **not** a full language model. It simply performs a very basic
search. You can extend it by integrating an open-source language model or
embedding-based retrieval library (e.g. `sentence-transformers`).

Usage::

    python offline_bot.py data_dir "your question here"

"""
import sys
from pathlib import Path
import re


def load_sentences(data_dir):
    """Load sentences from all .txt files under data_dir."""
    sentences = []
    for path in Path(data_dir).rglob('*.txt'):
        text = path.read_text(encoding='utf-8')
        for line in text.splitlines():
            line = line.strip()
            if line:
                sentences.append((path.name, line))
    return sentences


def simple_search(sentences, query):
    """Return sentences containing all keywords from the query."""
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
