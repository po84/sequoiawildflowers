from django.test import TestCase
from .models import Family, FamilyCommonName, ImageInfo
from .models import ColorRange, Plant, PlantCommonName
# Create your tests here.


class PlantCommonNameMethodTests(TestCase):
    def test_is_primary_common_name_with_primary_set_to_true(self):
        """
        is_primary_common_name() should return True for common names whose
        primary arribute is True.
        """
        plant_common_name = PlantCommonName(primary=True)
        self.assertEqual(plant_common_name.is_primary_common_name(), True)

    def test_is_primary_common_name_with_primary_set_to_false(self):
        """
        is_primary_common_name() should return False for common names whose
        primary arribute is False.
        """
        plant_common_name = PlantCommonName(primary=False)
        self.assertEqual(plant_common_name.is_primary_common_name(), False)


class ImageInfoMethodTests(TestCase):
    def test_is_landscape_orientation_with_landscape_image(self):
        """
        is_landscape_orientation() should return True for images whose width
        is larger than its height.
        """
        image_info = ImageInfo(image_width=300, image_height=200)
        self.assertEqual(image_info.is_landscape_orientation(), True)

    def test_is_landscape_orientation_with_portrait_image(self):
        """
        is_landscape_orientation() should return False for images whose width
        is smaller than its height.
        """
        image_info = ImageInfo(image_width=200, image_height=300)
        self.assertEqual(image_info.is_landscape_orientation(), False)

    def test_is_primary_image_with_primary_set_to_true(self):
        """
        is_primary_image() should return True for images whose primary
        arribute is True.
        """
        image_info = ImageInfo(primary=True)
        self.assertEqual(image_info.is_primary_image(), True)

    def test_is_primary_image_with_primary_set_to_false(self):
        """
        is_primary_image() should return False for images whose primary
        arribute is False.
        """
        image_info = ImageInfo(primary=False)
        self.assertEqual(image_info.is_primary_image(), False)
