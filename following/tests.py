from django.test import TestCase
from .models import *
from . import views
from django.test import RequestFactory
import json

# Create your tests here.

class UserTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_can_create_user(self):
        request = self.factory.get('/api/create_user')
        response = views.create_user(request)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['status'], 'success')
        # Make sure that user exists in the database
        self.assertEquals(CustomUser.objects.filter(
            pk=response_json['user_id']).count(), 1)

    def test_users_have_sequential_ids(self):
        request = self.factory.get('/api/create_user')
        response = views.create_user(request)
        first_user = json.loads(response.content)
        response = views.create_user(request)
        second_user = json.loads(response.content)
        self.assertLess(first_user['user_id'], second_user['user_id'])


class FollowTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = CustomUser()
        self.user1.save()
        self.user2 = CustomUser()
        self.user2.save()
        self.user3 = CustomUser()
        self.user3.save()
        self.unused_id = 100


    def test_can_follow(self):
        request = self.factory.post('/api/follow_user', data={
            'follower': self.user1.pk, 'following': self.user2.pk})
        response = views.follow_user(request)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['status'], 'success')
        # Check that this follow exists in the database
        self.assertEquals(Follow.objects.filter(
            follower=self.user1, following=self.user2).count(), 1)

    def test_double_follow_fails_gracefully(self):
        request = self.factory.post('/api/follow_user', data={
            'follower': self.user1.pk, 'following': self.user2.pk})
        _ = views.follow_user(request)  # Unused
        second_response = views.follow_user(request)
        response_json = json.loads(second_response.content)
        self.assertEquals(response_json['status'], 'fail')
        # Make sure they're still following that user
        self.assertEquals(Follow.objects.filter(
            follower=self.user1, following=self.user2).count(), 1)

    def test_invalid_following(self):
        request = self.factory.post('/api/follow_user', data={
            'follower': self.user1.pk, 'following': self.unused_id})
        response = views.follow_user(request)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['status'], 'fail')
        # Check that this follow doesn't exist in the database
        self.assertEquals(Follow.objects.filter(
            follower=self.user1, following__pk=self.unused_id).count(), 0)

    def test_invalid_follower(self):
        request = self.factory.post('/api/follow_user', data={
            'follower': self.unused_id, 'following': self.user1.pk})
        response = views.follow_user(request)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['status'], 'fail')
        # Check that this follow doesn't exist in the database
        self.assertEquals(Follow.objects.filter(
            follower__pk=self.unused_id, following=self.user1).count(), 0)

    def test_follow_get_request_fails_gracefully(self):
        request = self.factory.get('/api/follow_user')
        response = views.follow_user(request)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['status'], 'fail')

class UnfollowTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = CustomUser()
        self.user1.save()
        self.user2 = CustomUser()
        self.user2.save()
        self.user3 = CustomUser()
        self.user3.save()
        self.unused_id = 100
        self.user1.follow(self.user2)
        self.assertEquals(Follow.objects.filter(
            follower=self.user1, following=self.user2).count(), 1)

    def test_can_unfollow(self):
        request = self.factory.post('/api/unfollow_user', data={
            'follower': self.user1.pk, 'following': self.user2.pk})
        response = views.unfollow_user(request)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['status'], 'success')
        # Check that this follow is deleted from the database
        self.assertEquals(Follow.objects.filter(
            follower=self.user1, following=self.user2).count(), 0)

    def test_unfollow_twice_fails_gracefully(self):
        request = self.factory.post('/api/unfollow_user', data={
            'follower': self.user1.pk, 'following': self.user2.pk})
        _ = views.unfollow_user(request)
        response = views.unfollow_user(request)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['status'], 'fail')
        # Check that this follow is still deleted from the database
        self.assertEquals(Follow.objects.filter(
            follower=self.user1, following=self.user2).count(), 0)


    def test_unfollow_when_not_following_fails_gracefully(self):
        request = self.factory.post('/api/unfollow_user', data={
            'follower': self.user1.pk, 'following': self.user3.pk})
        response = views.unfollow_user(request)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['status'], 'fail')

    def test_invalid_follower_fails_gracefully(self):
        request = self.factory.post('/api/unfollow_user', data={
            'follower': self.unused_id, 'following': self.user1.pk})
        response = views.unfollow_user(request)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['status'], 'fail')

    def test_invalid_following_fails_gracefully(self):
        request = self.factory.post('/api/unfollow_user', data={
            'follower': self.user1.pk, 'following': self.unused_id})
        response = views.unfollow_user(request)
        response_json = json.loads(response.content)
        self.assertEquals(response_json['status'], 'fail')
