import unittest
from scripts.offline_bot import simple_search


class TestSimpleSearch(unittest.TestCase):
    """اختبارات دالة البحث البسيط.

    تغطي الحالات الاعتيادية والخالية والخاطئة.
    """

    def setUp(self):
        self.sentences = [
            ("a.txt", "hello world"),
            ("b.txt", "goodbye world"),
        ]

    def test_match(self):
        """يجب إرجاع الجملة المطابقة."""
        results = simple_search(self.sentences, "hello")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "hello world")

    def test_no_match(self):
        """بحث لا يعطي أي نتيجة."""
        results = simple_search(self.sentences, "unknown")
        self.assertEqual(results, [])

    def test_empty_query(self):
        """عند الاستعلام الفارغ يرجع كل الجمل."""
        results = simple_search(self.sentences, "")
        self.assertEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
