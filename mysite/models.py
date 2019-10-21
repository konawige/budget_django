from django.db import models

# Create your models here.

class BdgTypes(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Type"
    
    def __str__(self):
        return self.name

class AccountTypes(models.Model):
    name = models.CharField(max_length=20, default='none')


    class Meta:
        verbose_name = "Account Type"
    
    def __str__(self):
        return self.name

class BdgCategories(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Category"
    
    def __str__(self):
        return self.name


class BdgItems(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey('BdgCategories', on_delete=models.PROTECT)
    bdgType = models.ForeignKey('BdgTypes', on_delete=models.PROTECT)
    expected_amount = models.IntegerField()

    class Meta:
        verbose_name = "Item"

    def __str__(self):
        return self.name


class Entries(models.Model):
    date = models.DateField()
    amount = models.IntegerField()
    description = models.CharField(max_length=64)
    accountType = models.ForeignKey('AccountTypes', on_delete=models.PROTECT)
    item = models.ForeignKey('BdgItems', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Logging"

    def __str__(self):
        return "Entry"






