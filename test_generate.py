import unittest
import generate
import filecmp
import os
import shutil
from unittest import mock

class TestGenerate(unittest.TestCase):

	def setUp(self):
		self.input = "testin"
		self.output = "testout"
		os.mkdir(self.input)
		os.mkdir(self.output)

	def tearDown(self):
		shutil.rmtree(self.input)
		shutil.rmtree(self.output)

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

	def test_list_files(self):
		for i in range(1, 15):
			if i % 2 == 0:
				# create some non-rst files too
				with open(os.path.join(self.output, "nonrst_file_" + str(i)), "w") as f:
					pass
			# create 15 rst files
			with open(os.path.join(self.output, "test_file_" + str(i) + ".rst"), "w") as f:
				pass

		num_rst = 0
		for file, basename in generate.list_files(self.output):
			num_rst += 1

		self.assertTrue(num_rst == i, "Test fail: list_files() fails to list correct number of .rst files")

	def test_write_output(self):
		for i in range(1, 15):
			generate.write_output(str(i), "content of html here", self.output)

		for name in os.listdir(self.output):
			f = open(os.path.join(self.output, name), 'r')
			self.assertTrue(f.read() == "content of html here", "Test fail: write_output() writes wrong content to files")
			f.close()
			base, ext = os.path.splitext(name)
			self.assertTrue(ext == ".html", "Test fail: write_output() doesn't write .html files")

# to be able to just run `python test_generate.py` directly
if __name__ == '__main__':
	unittest.main()