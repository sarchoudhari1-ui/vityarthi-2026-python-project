import unittest

from radiation_estimator import estimate


class RadiationEstimatorTests(unittest.TestCase):
    def test_energy_uses_power_and_time(self):
        result = estimate("wifi", 60)
        self.assertAlmostEqual(result["energy_wh"], 0.10)

    def test_gps_is_receive_only_in_model(self):
        result = estimate("gps", 30)
        self.assertEqual(result["function"].transmit_power_w, 0.0)
        self.assertEqual(result["energy_wh"], 0.0)

    def test_negative_duration_is_rejected(self):
        with self.assertRaises(ValueError):
            estimate("call", -1)

    def test_unknown_function_is_rejected(self):
        with self.assertRaises(ValueError):
            estimate("microwave", 10)


if __name__ == "__main__":
    unittest.main()