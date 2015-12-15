from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Family(models.Model):
    scientific_name = models.CharField(max_length=100)
    icon_file_name = models.CharField(max_length=75)

    def __str__(self):
        return self.scientific_name


@python_2_unicode_compatible
class FamilyCommonName(models.Model):
    common_name = models.CharField(max_length=100)
    faimly = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self):
        return self.common_name


@python_2_unicode_compatible
class ColorRange(models.Model):
    color_range = models.CharField(max_length=50)
    icon_file_name = models.CharField(max_length=75)

    def __str__(self):
        return self.color_range


@python_2_unicode_compatible
class Plant(models.Model):
    scientific_name = models.CharField(max_length=100)
    plant_type = models.CharField(max_length=50)
    date_added = models.DateField()
    faimly = models.ForeignKey(Family)

    def __str__(self):
        return self.scientific_name


@python_2_unicode_compatible
class PlantCommonName(models.Model):
    common_name = models.CharField(max_length=100)
    primary_common_name = models.BooleanField()
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return self.common_name


@python_2_unicode_compatible
class ImageInfo(models.Model):
    file_name = models.CharField(max_length=75)
    image_width = models.IntegerField()
    image_height = models.IntegerField()
    primary_image = models.BooleanField()
    plant = models.ForeignKey(Plant)
    color_range = models.ForeignKey(ColorRange)

    def __str__(self):
        return self.file_name
