import unittest
from verifier import verify_news

class TestVerifier(unittest.TestCase):

    def test_verify_news(self):
        # This is a dummy test - it just checks the function runs without crashing
        label, scores, articles = verify_news("India signs new space treaty")
        self.assertIn(label, ["Likely True", "Likely False", "Needs Verification"])
        self.assertIsInstance(scores, list)
        self.assertIsInstance(articles, list)

if __name__ == "__main__":
    unittest.main()
 
