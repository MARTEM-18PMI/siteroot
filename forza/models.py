from django.db.models import *
from django.contrib.auth.models import User
from django.urls import reverse
DEFAULT = 'default.jpg'


class Blog(Model):
    title = CharField(max_length=80)
    created_at = DateTimeField('timestamp creation', auto_now_add=True)
    author = ForeignKey(User, on_delete=CASCADE, default=1)

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_absolute_url(self):
        return reverse("blog_by_id", kwargs={'blog_id': self.id})


class Post(Model):
    blog = ForeignKey(Blog, on_delete=CASCADE)
    subject = CharField(max_length=80)
    text = TextField(max_length=4096)

    created_at = DateTimeField('timestamp of creation', auto_now_add=True)
    updated_at = DateTimeField('timestamp of update', auto_now=True)

    def __str__(self):
        return str(self.subject)

    def get_absolute_url(self):
        return reverse("blog_by_id", kwargs={'blog_id': self.id})
