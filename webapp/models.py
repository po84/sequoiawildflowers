from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Family(models.Model):
    scientific_name = models.CharField(max_length=100)
    icon_file_name = models.CharField(max_length=75)

    def __str__(self):
        return self.scientific_name

    def _get_formatted_common_names(self):
        common_names = self.familycommonname_set.all()
        number_of_common_names = len(common_names)
        if number_of_common_names == 0:
            return None
        elif number_of_common_names == 1:
            return common_names[0].common_name
        elif number_of_common_names == 2:
            common_name_string = common_names[0].common_name
            common_name_string += " or "
            common_name_string += common_names[1].common_name
            return common_name_string
        else:
            common_name_list = [(item.common_name) for item in common_names]
            last_common_name = common_name_list[-1]
            rest_of_common_names = common_name_list[:-1]
            common_name_string = ", ".join(rest_of_common_names)
            common_name_string += " or "
            common_name_string += last_common_name
            return common_name_string
    formatted_common_names = property(_get_formatted_common_names)


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
    family = models.ForeignKey(Family)
    image_colors = models.ManyToManyField(ColorRange, through='ImageInfo')

    def __str__(self):
        return self.scientific_name

    def _get_formatted_common_names(self):
        common_names = self.plantcommonname_set.all()
        number_of_common_names = len(common_names)
        if number_of_common_names == 0:
            return None
        elif number_of_common_names == 1:
            return common_names[0].common_name
        elif number_of_common_names == 2:  # need to put primary name first
            primary_name = (common_names
                            .filter(primary=True)
                            .get()
                            .common_name)
            other_name = (common_names
                          .filter(primary=False)
                          .get()
                          .common_name)
            common_name_string = primary_name
            common_name_string += " or "
            common_name_string += other_name
            return common_name_string
        else:  # need to put primary name first
            primary_name = (common_names
                            .filter(primary=True)
                            .get()
                            .common_name)
            other_names = (common_names
                           .filter(primary=False)
                           .all())
            other_name_list = [(item.common_name) for item in other_names]
            last_other_name = other_name_list[-1]
            rest_of_other_names = other_name_list[:-1]
            other_name_string = ", ".join(rest_of_other_names)
            other_name_string += " or "
            other_name_string += last_other_name
            return primary_name + ", " + other_name_string

    def _get_primary_common_name(self):
        primary_name = (self.plantcommonname_set
                            .filter(primary=True)
                            .get()
                            .common_name)
        return primary_name

    def _get_primary_image_file_name(self):
        primary_image_file_name = (self.imageinfo_set
                                   .filter(primary=True)
                                   .all())
        if len(primary_image_file_name) == 0:
            return None
        else:
            return primary_image_file_name[0].file_name

    formatted_common_names = property(_get_formatted_common_names)
    primary_common_name = property(_get_primary_common_name)
    primary_image_file_name = property(_get_primary_image_file_name)


@python_2_unicode_compatible
class PlantCommonName(models.Model):
    common_name = models.CharField(max_length=100)
    primary = models.BooleanField()
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return self.common_name


@python_2_unicode_compatible
class ImageInfo(models.Model):
    file_name = models.CharField(max_length=75)
    image_width = models.IntegerField()
    image_height = models.IntegerField()
    primary = models.BooleanField()
    plant = models.ForeignKey(Plant)
    color_range = models.ForeignKey(ColorRange)

    def __str__(self):
        return self.file_name

    def is_landscape_orientation(self):
        return True if (self.image_width >= self.image_height) else False

    def is_primary_image(self):
        return self.primary
