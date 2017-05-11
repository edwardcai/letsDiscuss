from __future__ import unicode_literals

from django.db import models

class Categories(models.Model):
    id = models.CharField(primary_key=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'categories'

class RestaurantCategories(models.Model):
    business_id = models.CharField(max_length=30, blank=True, null=True)
    category_id = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurant_categories'


class Restaurants(models.Model):
    id = models.CharField(primary_key=True, max_length=30, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurants'


class ReviewTokens(models.Model):
    review = models.ForeignKey('Reviews', models.DO_NOTHING, blank=True, null=True)
    words = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_tokens'


class Reviews(models.Model):
    business_id = models.CharField(max_length=30, blank=True, null=True)
    stars = models.IntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'
