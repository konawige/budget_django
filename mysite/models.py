from django.db import models

# Create your models here.

class Types(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'types'

class Categories(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'categories'

class Items(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey('Categories', models.DO_NOTHING)
    type_entry = models.ForeignKey('Types', models.DO_NOTHING)
    expected_amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'items'


class Entries(models.Model):
    date = models.DateField()
    amount = models.IntegerField()
    item = models.ForeignKey('Items', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'entries'






