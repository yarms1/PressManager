from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from press_hub.models import Topic, Newspaper


class PressHubTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.staff_user = User.objects.create_user(username='staffuser',
                                                   password='testpassword')
        self.staff_user.is_staff = True
        self.staff_user.save()

        self.topic = Topic.objects.create(name='Test Topic')

    def test_homepage_loads(self):
        response = self.client.get(reverse('press_hub:home'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_access_topic_list(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('press_hub:topic-list'))
        self.assertEqual(response.status_code, 200)
