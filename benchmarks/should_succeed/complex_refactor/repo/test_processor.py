import unittest
from legacy_processor import LegacyProcessor

class TestLegacyProcessor(unittest.TestCase):
    def setUp(self):
        self.config = {'version': 2}
        self.processor = LegacyProcessor(self.config)

    def test_valid_data_processing(self):
        data = [
            {'id': 1, 'value': '  Hello World!  '},
            {'id': 2, 'value': 'Testing 123...'}
        ]
        results = self.processor.process_data(data)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['clean_value'], 'hello world')
        self.assertEqual(results[0]['status'], 'processed')
        self.assertEqual(results[0]['version'], 2)
        
        self.assertEqual(results[1]['clean_value'], 'testing 123')

    def test_validation_skips_invalid(self):
        data = [
            {'id': 1, 'value': 'ok'},
            'not a dict',
            {'value': 'missing id'},
            {'id': -5, 'value': 'negative id'}
        ]
        results = self.processor.process_data(data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 1)

    def test_truncation(self):
        long_str = "a" * 150
        data = [{'id': 1, 'value': long_str}]
        results = self.processor.process_data(data)
        self.assertEqual(len(results[0]['clean_value']), 100)

if __name__ == '__main__':
    unittest.main()
