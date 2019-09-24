import unittest
from app.models import Post
from app import db

class PostModelTest(unittest.TestCase):
    def setUp(self):
        self.user_gideon = User(username = 'Gideon',password = 'password', email = 'gideon@ms.com')
        self.new_pitch = Post(id=1,title='Test',date_posted='2018/3/3', content="interview",user_id = "3")

    def tearDown(self):
        Post.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_post.title,'Test')
        self.assertEquals(self.new_post.date_posted,'4/6/2017')
        self.assertEquals(self.new_post.content,"interview")
        self.assertEquals(self.new_post.user_id="4")

    def test_save_pitch(self):
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all())>0)

    def test_get_pitch_by_id(self):
        self.new_post.save_post()
        got_post = Post.get_post(1)
        self.assertTrue(got_post is not None) 