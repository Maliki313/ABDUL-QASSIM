import json
from pathlib import Path
from scripts import parse_history

def test_extract_text_from_mapping():
    mapping = {
        '1': {'create_time': 1, 'message': {'content': {'parts': ['مرحبا']}}},
        '2': {'create_time': 2, 'message': {'content': {'parts': ['هلا']}}},
    }
    texts = list(parse_history.extract_text_from_mapping(mapping))
    assert texts == ['مرحبا', 'هلا']

def test_write_conversation(tmp_path):
    conv = {
        'title': 'test',
        'mapping': {
            '1': {'create_time': 1, 'message': {'content': {'parts': ['اهلا']}}}
        },
    }
    parse_history.write_conversation(conv, tmp_path)
    text = (tmp_path / 'test.txt').read_text(encoding='utf-8').strip()
    assert text == 'اهلا'


def test_slugify_and_sanitized_filename(tmp_path):
    conv = {
        'title': 'my convo *1?',
        'mapping': {
            '1': {'create_time': 1, 'message': {'content': {'parts': ['hi']}}}
        },
    }
    parse_history.write_conversation(conv, tmp_path)
    files = list(tmp_path.iterdir())
    assert files[0].name == 'my_convo_1.txt'

