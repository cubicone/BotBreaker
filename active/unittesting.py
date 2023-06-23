from Security2 import Security2
from Blog2 import Blog2
import unittest

sec = Security2("botbreaker")
sec.loadCredentials()
blog = Blog2(sec)


# print(blog.info("botbreaker", ["name"]).json())
# quit()


class InfoTestCase(unittest.TestCase):
    # passes when just blogname given
    def test_basic_pass(self):
        result = str(blog.info("botbreaker"))
        self.assertEqual(result, "<Response [200]>")

    # passes when blogname and valid field given
    def test_field_pass(self):
        result = str(blog.info("teamredpointone", ["name"]))
        self.assertEqual(result, "<Response [200]>")

    # passes when blogname and empty field given
    def test_empty_field_pass(self):
        result = str(blog.info("botbreaker", []))
        self.assertEqual(result, "<Response [200]>")

    # fails when empty blogname given
    def test_blog_empty_fail(self):
        result = str(blog.info(""))
        self.assertEqual(result, "<Response [404]>")

    # fails when dud blogname given
    def test_blog_dud_fail(self):
        result = str(blog.info("otbreaker"))
        self.assertEqual(result, "<Response [404]>")


class AvatarTestCase(unittest.TestCase):
    # passes when blogname given
    def test_blog_pass(self):
        result = str(blog.avatar("botbreaker"))
        self.assertEqual(result, "<Response [200]>")

    # passes when blogname and approp size given
    def test_blog_size_pass(self):
        result = str(blog.avatar("botbreaker", 64))
        self.assertEqual(result, "<Response [200]>")

    # fails when no blogname given
    def test_no_blog_fail(self):
        result = str(blog.avatar(""))
        self.assertEqual(result, "<Response [404]>")

    # API QUIRK
    # # fails when size given as inappro value
    # def test_inappro_size_fail(self):
    #     result = str(blog.avatar("botbreaker", -1000))
    #     self.assertEqual(result, "<Response [200]>") #DONT ASK

    # DEVELOPER NOTE:
    # When given a value that is not 64px or a larger format (128, 512),
    # size is completely ignored??? for some reason???? tumblr why...


class BlockedListTestCase(unittest.TestCase):
    # passes when blogname given
    def test_blog_pass(self):
        result = str(blog.blockedList("botbreaker"))
        self.assertEqual(result, "<Response [200]>")


print(blog.blockedList("botbreaker").json())
quit()

unittest.main()
