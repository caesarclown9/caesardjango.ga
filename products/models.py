from django.conf import settings
from django.db import models
from django.utils.text import slugify

from users.models import User

from .managers import ProductManager


CURRENCY = settings.CURRENCY

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
        return f"{self.title} - {self.id}"



class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    image = models.ImageField(blank=True, null=True)
    value = models.DecimalField(max_digits=10,  decimal_places=2, null=False, blank=False)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    active = models.BooleanField(default=False)
    qty = models.PositiveIntegerField(null=False, blank=False)
    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    browser = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        self.final_value = self.value - self.discount_value if self.discount_value > 0 else self.value
        super().save(*args, **kwargs)

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'
    tag_final_value.short_description = 'Value'


    def __str__(self):
        return f"{self.title} - {self.id}"

class Wish(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product} --> {self.user}'


class Bucketlist(models.Model):
    """ Bucketlist model class """
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=100, blank=True, default='None')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bucketlists')

    def __unicode__(self):
        return "{} : {}".format(self.id, self.name)

    class Meta:
        unique_together = ("name", "created_by")


class BucketlistItem(models.Model):
    """ Bucketlist item model class """
    item_name = models.CharField(max_length=50, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    bucketlist = models.ForeignKey(Bucketlist, on_delete=models.CASCADE, related_name='bucketlist_items')
    is_done = models.BooleanField(default=False)

    def __unicode__(self):
        return "{}".format(self.item_name)

    class Meta:
        unique_together = ("item_name", "bucketlist")
