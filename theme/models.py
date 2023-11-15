from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post_title = models.CharField(max_length=200)
    post_text = models.TextField()
    pub_date = models.DateTimeField('pub_date', default=timezone.now)
    slug = models.SlugField(unique=True)
    view_count = models.PositiveIntegerField('view_count', default=0, blank=True)
    like_count = models.ManyToManyField(User, related_name='like')

    def generate_slug(self):
        return slugify(self.post_title)

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse("theme:detail", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("theme:like-toggle", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse("theme:like-api-toggle", kwargs={"slug": self.slug})

    def get_edit_url(self):
        return reverse('theme:edit', kwargs={'slug': self.slug})


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    pub_date = models.DateTimeField('pub_date', default=timezone.now)

    def __str__(self):
        return self.comment_text
