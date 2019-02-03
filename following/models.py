from django.db import models

# Create your models here.


class CustomUser(models.Model):
    def follow(self, other):
        # Test that they're not already following this user.
        if Follow.objects.filter(follower=self, following=other).count() > 0:
            return {'status': 'fail',
                    'reason': 'User {} is already following User {}'.format(
                        self.pk, other.pk)}
        # Make sure they haven't blocked this user
        elif Block.objects.filter(blocker=self, blocked_user=other).count() > 0:
            return {'status': 'fail',
                    'reason': 'User {} has blocked User {}'.format(
                        self.pk, other.pk)}
        # Make sure they aren't blocked
        elif Block.objects.filter(blocker=self, blocked_user=other).count() > 0:
            return {'status': 'fail',
                    'reason': 'Unexpected Error Occurred'}  # Ambiguous Error
        f = Follow(follower=self, following=other)
        f.save()
        return {'status': 'success'}

    def unfollow(self, other):
        # Test that they are following this user.
        follow_list = Follow.objects.filter(follower=self, following=other)
        if len(follow_list) == 0:
            return {'status': 'fail',
                    'reason': 'User {} is not following User {}'.format(
                        self.pk, other.pk)}
        follow = follow_list.first()
        follow.delete()
        return {'status': 'success'}


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 related_name='users_you_are_following')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  related_name='users_following_you')

    def __str__(self):
        return "{} following {}".format(self.follower.pk, self.following.pk)

    class Meta:
        unique_together = ("follower", "following")


class Block(models.Model):
    blocker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users_you_are_blocking')
    blocked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("blocker", "blocked_user")
