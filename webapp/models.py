from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Family(models.Model):
    scientific_name = models.CharField(max_length=200)

    def __str__(self):
        return self.scientific_name


@python_2_unicode_compatible
class FamilyCommonName(models.Model):
    faimly = models.ForeignKey(Family, on_delete=models.CASCADE)
    common_name = models.CharField(max_length=200)

    def __str__(self):
        return self.common_name
