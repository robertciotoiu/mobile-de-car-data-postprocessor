import unittest
import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from post_processors.power_pp import PowerPostProcessor

class TestPowerPostProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = PowerPostProcessor()

    def test_convert_to_hp_with_valid_power(self):
        car = {'power': '170 kW (231 hp)'}
        result = self.processor.convert_to_hp(car)
        self.assertEqual(result, 231)

    def test_convert_to_hp_with_only_kw(self):
        car = {'power': '170 kW'}
        result = self.processor.convert_to_hp(car)
        self.assertEqual(result, 227)  # 170 kW * 1.341 ≈ 227 HP

    def test_convert_to_hp_with_invalid_power(self):
        car = {'power': '170'}
        result = self.processor.convert_to_hp(car)
        self.assertIsNone(result)

    def test_convert_to_hp_with_empty_power(self):
        car = {'power': ''}
        result = self.processor.convert_to_hp(car)
        self.assertIsNone(result)

    def test_process_with_valid_power(self):
        car = {'power': '170 kW (231 hp)'}
        processed_car = self.processor.process(car)
        self.assertEqual(processed_car['power'], 231)

    def test_process_with_only_kw(self):
        car = {'power': '170 kW'}
        processed_car = self.processor.process(car)
        self.assertEqual(processed_car['power'], 227)  # 170 kW * 1.341 ≈ 227 HP

    def test_process_with_invalid_power(self):
        car = {'power': '170'}
        processed_car = self.processor.process(car)
        self.assertIsNone(processed_car['power'])

    def test_process_with_empty_power(self):
        car = {'power': ''}
        processed_car = self.processor.process(car)
        self.assertIsNone(processed_car['power'])

if __name__ == '__main__':
    unittest.main()