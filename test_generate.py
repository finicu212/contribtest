import unittest
import generate
import filecmp
import os
import shutil
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

	def prep_test(self, test_location):
		if not os.path.exists(test_location):
			os.mkdir(test_location)
		else:
			print(test_location + " already exists. aborting...")
			quit()

	def test_list_files(self):
		test_location = "test_listing"
		self.prep_test(test_location)

		for i in range(1, 15):
			if i % 2 == 0:
				# create some non-rst files too
				with open(os.path.join(test_location, "nonrst_file_" + str(i)), "w") as f:
					pass
			# create 15 rst files
			with open(os.path.join(test_location, "test_file_" + str(i) + ".rst"), "w") as f:
				pass

		num_rst = 0
		for file, basename in generate.list_files(test_location):
			num_rst += 1
		# get rid of the directory when we're done counting
		shutil.rmtree(test_location)
		self.assertTrue(num_rst == i, "Test fail: list_files() fails to list correct number of .rst files")

# to be able to just run `python test_generate.py` directly
if __name__ == '__main__':
	unittest.main()