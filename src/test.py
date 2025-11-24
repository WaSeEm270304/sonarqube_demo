
import unittest
from unittest.mock import patch
from main import add, subtract, multiply, divide, calculator

class TestCalculator(unittest.TestCase):

    # ------------------- ADD -------------------
    def test_add(self):
        self.assertEqual(add(3, 4), 7)
        self.assertEqual(add(-1, 5), 4)
        self.assertAlmostEqual(add(2.5, 1.2), 3.7)

    # ------------------- SUBTRACT -------------------
    def test_subtract(self):
        self.assertEqual(subtract(10, 3), 7)
        self.assertEqual(subtract(0, 5), -5)
        self.assertAlmostEqual(subtract(5.5, 2.2), 3.3)

    # ------------------- MULTIPLY -------------------
    def test_multiply(self):
        self.assertEqual(multiply(4, 5), 20)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertAlmostEqual(multiply(2.5, 2), 5.0)
        self.assertEqual(multiply(5, 0), 0)

    # ------------------- DIVIDE -------------------
    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertAlmostEqual(divide(7.5, 2.5), 3.0)
        self.assertEqual(divide(-10, 2), -5)
        self.assertEqual(divide(10, -2), -5)
        self.assertEqual(divide(-10, -2), 5)

    def test_divide_by_zero(self):
        self.assertEqual(divide(5, 0), "Error: Cannot divide by zero!")
        self.assertEqual(divide(0, 0), "Error: Cannot divide by zero!")

    # ------------------- FULL CALCULATOR INTERACTIVE TEST -------------------
    @patch('builtins.input', side_effect=['10', '5', '+'])
    @patch('builtins.print')
    def test_calculator_add(self, mock_print, mock_input):
        calculator()
        mock_print.assert_any_call(15)

    @patch('builtins.input', side_effect=['10', '5', '-'])
    @patch('builtins.print')
    def test_calculator_subtract(self, mock_print, mock_input):
        calculator()
        mock_print.assert_any_call(5)

    @patch('builtins.input', side_effect=['10', '5', '*'])
    @patch('builtins.print')
    def test_calculator_multiply(self, mock_print, mock_input):
        calculator()
        mock_print.assert_any_call(50)

    @patch('builtins.input', side_effect=['10', '5', '/'])
    @patch('builtins.print')
    def test_calculator_divide(self, mock_print, mock_input):
        calculator()
        mock_print.assert_any_call(2.0)

    @patch('builtins.input', side_effect=['10', '0', '/'])
    @patch('builtins.print')
    def test_calculator_divide_by_zero(self, mock_print, mock_input):
        calculator()
        mock_print.assert_any_call("Error: Cannot divide by zero!")

    @patch('builtins.input', side_effect=['10', '5', '^'])
    @patch('builtins.print')
    def test_calculator_invalid_op(self, mock_print, mock_input):
        calculator()
        mock_print.assert_any_call("Invalid operation!")

if __name__ == "__main__":
    unittest.main()
