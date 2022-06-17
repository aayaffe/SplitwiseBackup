import filecmp
import os
import shutil
import unittest


class TestUtils(unittest.TestCase):
    def setUp(self):
        os.chdir("../..")

    def test_file_copy_rename(self):
        import utils
        src = 'tests/unit/files/test1.txt'
        dst_dir = 'tests/unit/files/newdir/'
        dst_file_name = 'test2'
        utils.file_copy_rename(src, dst_dir, dst_file_name)
        self.assertTrue(filecmp.cmp(src, os.path.join(dst_dir,dst_file_name)+".txt", shallow=False))
        shutil.rmtree(dst_dir)


if __name__ == '__main__':
    unittest.main()
