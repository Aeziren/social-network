from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    qtt_likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user}' post"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user}'s likes on {self.post.user}'s post"


class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    to_user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.from_user} following on {self.to_user}"
