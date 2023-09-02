from django.test import TestCase,Client
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post
from django.urls import reverse


class DBTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='neelima',password='NEel123@')
        self.client = Client()
        self.client.login(username='neelima', password='NEel123@')


    def test_Create(self):
        post1 = Post.objects.create(
            title='Python1',
            content='Pyhton1 is the 1nd post',
            published_at=timezone.now(),
            author=self.user,
        )
        # if the post created is an object of Pst table only
        self.assertTrue(isinstance(post1, Post))

    def test_title(self):
        post1 = Post.objects.create(
            title='Python1',
            content='Pyhton1 is the 1nd post',
            published_at=timezone.now(),
            author=self.user,
        )
        # if the post created is an object of Pst table only
        self.assertTrue(post1.title,'Python')

    def test_publishIsNone(self):
        post1 = Post.objects.create(
            title='Python1',
            content='Pyhton1 is the 1nd post',
            author=self.user,
        )
        self.assertIsNotNone(post1.published_at) 

    def test_publish_order(self):
        post3 = Post.objects.create(
            title='Python3',
            content='Pyhton1 is the 1nd post',
            published_at='2023-08-29 14:30:00',
            author=self.user,
        )
        post4 = Post.objects.create(
            title='Python4',
            content='Pyhton2 is the 2nd post',
            published_at='2023-08-27 14:30:00',
            author=self.user,
        )
        self.assertEqual(list(Post.objects.all()), [post3, post4])

    def test_home(self):
        post1 = Post.objects.create(
        title='Python1',
        content='Pyhton1 is the 1nd post',
        published_at=timezone.now(),
        author=self.user,
        )
        response = self.client.get(reverse('home'))
        self.assertContains(response,'Python1')

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response,'About')
    
    def test_createpost(self):
        data = {
            'title': 'Learning Django',
            'content': 'learning test cases in django'
        }
        response = self.client.post(reverse('post-create'), data, follow=True)
     
        # print(Post.objects.all())  # Print all objects in the Post table

        self.assertEqual(response.status_code, 200)

        # Verify the post creation in the database
        post_count = Post.objects.filter(title='Learning Django').count()
        self.assertEqual(post_count, 1)

    

    