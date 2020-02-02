from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.text import slugify


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='addresses')
    street = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)

    def __unicode__(self):
        return self.street

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.street)[:50]

        return super(Address, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    delivery_method = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=5, default=0)
    slug = models.SlugField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.name)[:50]

        return super(Order, self).save(*args, **kwargs)


class Burger(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='burgers')
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    body = models.TextField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.name)[:50]

        return super(Burger, self).save(*args, **kwargs)


class Ingredient(models.Model):
    burger = models.ForeignKey(Burger, on_delete=models.CASCADE, related_name='ingredients', null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    count = models.IntegerField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.name)[:50]

        return super(Ingredient, self).save(*args, **kwargs)
