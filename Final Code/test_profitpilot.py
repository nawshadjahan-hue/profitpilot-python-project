import unittest

import logic


class TestProfitPilotCalculations(unittest.TestCase):
    def setUp(self):
        self.products = [
            {"name": "Iced Matcha Latte", "cost": 3.20, "price": 7.50, "quantity": 45},
            {"name": "Bubble Tea", "cost": 4.20, "price": 8.00, "quantity": 38},
            {"name": "Phone Case", "cost": 4.00, "price": 15.00, "quantity": 12},
        ]
        for index, product in enumerate(self.products):
            self.products[index] = logic.calculate_metrics(product, self.products)

    def test_calculate_metrics_adds_business_values(self):
        product = {"name": "Banana Bread", "cost": 2.00, "price": 5.50, "quantity": 30}

        result = logic.calculate_metrics(product, [product])

        self.assertEqual(result["revenue"], 165.00)
        self.assertEqual(result["total_cost"], 60.00)
        self.assertEqual(result["profit"], 105.00)
        self.assertAlmostEqual(result["margin"], 63.6363636)
        self.assertIn("score", result)
        self.assertIn("status", result)
        self.assertIn("recommendation", result)

    def test_break_even_units_returns_required_units(self):
        product = {"name": "Coffee", "cost": 2.50, "price": 6.50, "quantity": 20}

        result = logic.break_even_units(product, fixed_cost=100)

        self.assertEqual(result, 25)

    def test_break_even_units_returns_none_when_no_contribution(self):
        product = {"name": "Discount Snack", "cost": 5.00, "price": 4.00, "quantity": 20}

        result = logic.break_even_units(product, fixed_cost=100)

        self.assertIsNone(result)

    def test_what_if_analysis_does_not_change_original_product(self):
        original_price = self.products[0]["price"]
        original_quantity = self.products[0]["quantity"]

        result = logic.what_if_analysis(self.products[0], self.products, new_price=7.90, new_quantity=48)

        self.assertEqual(self.products[0]["price"], original_price)
        self.assertEqual(self.products[0]["quantity"], original_quantity)
        self.assertEqual(result["price"], 7.90)
        self.assertEqual(result["quantity"], 48)
        self.assertGreater(result["profit"], self.products[0]["profit"])

    def test_business_break_even_uses_all_products(self):
        result = logic.business_break_even(self.products, fixed_cost=500)

        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_loss_making_product_is_at_risk(self):
        product = {"name": "Bad Deal", "cost": 10.00, "price": 8.00, "quantity": 10}

        result = logic.calculate_metrics(product, [product])

        self.assertLess(result["profit"], 0)
        self.assertEqual(result["status"], "At Risk")
        self.assertIn("losing money", result["recommendation"])

    def test_score_breakdown_matches_total_score(self):
        product = self.products[0]

        breakdown = logic.calculate_score_breakdown(product, self.products)

        self.assertEqual(breakdown["total"], product["score"])
        self.assertLessEqual(breakdown["profit"], 40)
        self.assertLessEqual(breakdown["margin"], 40)
        self.assertLessEqual(breakdown["demand"], 20)


if __name__ == "__main__":
    unittest.main()
