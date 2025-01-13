import unittest
from datetime import datetime
import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from post_processors.first_register_pp import FirstRegisterPostProcessor

class TestFirstRegisterPostProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = FirstRegisterPostProcessor()

    def test_convert_to_date_with_valid_date(self):
        car = {'firstRegister': '02/2020'}
        result = self.processor.convert_to_date(car)
        self.assertEqual(result, datetime(2020, 2, 1))

    def test_convert_to_date_with_invalid_date(self):
        car = {'firstRegister': 'invalid_date'}
        result = self.processor.convert_to_date(car)
        self.assertIsNone(result)

    def test_convert_to_date_with_empty_date(self):
        car = {'firstRegister': ''}
        result = self.processor.convert_to_date(car)
        self.assertIsNone(result)

    def test_process_with_valid_date(self):
        car = {'firstRegister': '02/2020'}
        processed_car = self.processor.process(car)
        self.assertEqual(processed_car['firstRegister'], datetime(2020, 2, 1))

    def test_process_with_invalid_date(self):
        car = {'firstRegister': 'invalid_date'}
        processed_car = self.processor.process(car)
        self.assertIsNone(processed_car['firstRegister'])

    def test_process_with_empty_date(self):
        car = {'firstRegister': ''}
        processed_car = self.processor.process(car)
        self.assertIsNone(processed_car['firstRegister'])

if __name__ == '__main__':
    unittest.main()