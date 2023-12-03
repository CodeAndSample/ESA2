import unittest
from ESA2.chancellor_simulator import get_high_scores


class MyTestCase(unittest.TestCase):
    def test_get_high_scores(self):
        high_scores = get_high_scores()
        for i, score in enumerate(high_scores):
            print(
                f"{i+1}. {score.player_name} - Stability: {score.stability} - Turns: {score.turns_taken}"
            )
        # first print equals to "1. Quirin - Stability: 10 - Turns: 0"
        self.assertEqual(high_scores[0].player_name, "Christian")


if __name__ == "__main__":
    unittest.main()
