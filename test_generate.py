import unittest
import generate
import filecmp

class TestGenerate(unittest.TestCase):
	def test_generate_site_from_example(self):
		result = generate.generate_site("test/source", "output")
		self.assertTrue(filecmp.cmp("output/index.html", "test/expected_output/index.html"), "Test fail: Unexpected output in index.html")
		self.assertTrue(filecmp.cmp("output/contact.html", "test/expected_output/contact.html"), "Test fail: Unexpected output in contact.html")

# to be able to just run `python test_generate.py` directly
if __name__ == '__main__':
	unittest.main()