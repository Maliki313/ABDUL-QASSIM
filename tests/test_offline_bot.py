from pathlib import Path
from scripts import offline_bot


def test_load_sentences(tmp_path):
    f = tmp_path / 'note.txt'
    f.write_text('hello\nworld', encoding='utf-8')
    sentences = offline_bot.load_sentences(tmp_path)
    assert sentences == [('note.txt', 'hello'), ('note.txt', 'world')]


def test_load_sentences_multiple_dirs(tmp_path):
    d1 = tmp_path / 'd1'
    d2 = tmp_path / 'd2'
    d1.mkdir()
    d2.mkdir()
    (d1 / 'a.txt').write_text('one', encoding='utf-8')
    (d2 / 'b.txt').write_text('two', encoding='utf-8')
    sentences = offline_bot.load_sentences([d1, d2])
    assert ('a.txt', 'one') in sentences and ('b.txt', 'two') in sentences


def test_simple_search():
    sentences = [('note.txt', 'python rules'), ('note.txt', 'use snake case')]
    result = offline_bot.simple_search(sentences, 'python')
    assert result == [('note.txt', 'python rules')]
    empty = offline_bot.simple_search(sentences, 'java')
    assert empty == []

