from django.db import models

from users.models import User




class Category(models.Model):
    title = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=30, blank=True, null=True, unique = True)


    def save(self):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


    def __str__(self):
        return self.title



class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    image = models.ImageField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


