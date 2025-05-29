import unittest
from app.utils import allowed_file

class TestUtils(unittest.TestCase):

    def test_allowed_extension_lower(self):
        self.assertTrue(allowed_file("image.jpg"), "Test failed for image.jpg")
        self.assertTrue(allowed_file("photo.png"), "Test failed for photo.png")
        self.assertTrue(allowed_file("animation.gif"), "Test failed for animation.gif")
        self.assertTrue(allowed_file("picture.jpeg"), "Test failed for picture.jpeg")

    def test_allowed_extension_upper(self):
        self.assertTrue(allowed_file("image.JPG"), "Test failed for image.JPG")
        self.assertTrue(allowed_file("photo.PnG"), "Test failed for photo.PnG")
        self.assertTrue(allowed_file("animation.GIF"), "Test failed for animation.GIF")
        self.assertTrue(allowed_file("picture.jPeG"), "Test failed for picture.jPeG")

    def test_disallowed_extension(self):
        self.assertFalse(allowed_file("document.pdf"), "Test failed for document.pdf")
        self.assertFalse(allowed_file("archive.zip"), "Test failed for archive.zip")
        self.assertFalse(allowed_file("script.py"), "Test failed for script.py")
        self.assertFalse(allowed_file("image.jpgx"), "Test failed for image.jpgx")

    def test_multiple_dots(self):
        self.assertTrue(allowed_file("image.backup.jpg"), "Test failed for image.backup.jpg")
        self.assertFalse(allowed_file("archive.tar.gz"), "Test failed for archive.tar.gz")
        self.assertTrue(allowed_file("photo.old.png"), "Test failed for photo.old.png")

    def test_no_extension(self):
        self.assertFalse(allowed_file("myfile"), "Test failed for 'myfile'")
        self.assertFalse(allowed_file("image"), "Test failed for 'image'")

    def test_only_extension(self):
        self.assertTrue(allowed_file(".jpg"), "Test failed for '.jpg'")
        self.assertTrue(allowed_file(".png"), "Test failed for '.png'")

    def test_hidden_file(self):
        self.assertFalse(allowed_file(".bashrc"), "Test failed for '.bashrc'")
        self.assertFalse(allowed_file(".gitconfig"), "Test failed for '.gitconfig'")

    def test_empty_or_dot_filename(self):
        self.assertFalse(allowed_file(""), "Test failed for empty string")
        self.assertFalse(allowed_file("."), "Test failed for '.'")

if __name__ == '__main__':
    unittest.main()
