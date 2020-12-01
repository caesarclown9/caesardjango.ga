from django.db import models
from django.utils.text import slugify

from users.models import User




class Category(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=30, blank=True, null=True, unique = True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} - {self.slug}"



class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    image = models.ImageField(blank=True, null=True)
    price = models.DecimalField(max_digits=10,  decimal_places=2)
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

