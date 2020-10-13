import unittest
import generate
import filecmp
import os
from unittest import mock

class TestGenerate(unittest.TestCase):
	def test_generate_site_from_example(self):
		source_dir = "test/source"
		expected_dir = "test/expected_output"
		output_dir = "output"
		result = generate.generate_site(source_dir, output_dir)

		# for each file which we expect
		for f in os.listdir(expected_dir):
			outputted_file = os.path.join(output_dir, f)
			# make sure that the file actually got created
			self.assertTrue(os.path.isfile(outputted_file), "File " + f + " did not get created!")
			# make sure that the file contents are identical
			self.assertTrue(filecmp.cmp(outputted_file, os.path.join(expected_dir, f)), "Test fail: Unexpected output in " + f)

	#@mock.patch('generate.read_file')
	#def test_reading(self, read_file_mock):
	#	with open("example.rst", "w") as f:
	#		f.write('{"title": "example", "layout": "example.html"} --- content example here')



# to be able to just run `python test_generate.py` directly
if __name__ == '__main__':
	unittest.main()