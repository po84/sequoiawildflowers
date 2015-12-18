from django.test import TestCase
from django.core.urlresolvers import reverse
from django.db.models import Count
from .models import Family, FamilyCommonName, ImageInfo
from .models import ColorRange, Plant, PlantCommonName
from datetime import date
import random
from PIL import Image


def create_database():
    family1 = Family.objects.create(scientific_name='family 1',
                                    icon_file_name='family_1_icon.jpg')
    family2 = Family.objects.create(scientific_name='family 2',
                                    icon_file_name='family_2_icon.jpg')

    family1.familycommonname_set.create(common_name='family 1 cn 1')
    family1.familycommonname_set.create(common_name='family 1 cn 2')
    family2.familycommonname_set.create(common_name='family 2 cn 1')
    family2.familycommonname_set.create(common_name='family 2 cn 2')

    plant1 = family1.plant_set.create(scientific_name='plant 1',
                                      plant_type='plant type',
                                      date_added=date(2012, 05, 20))
    plant2 = family1.plant_set.create(scientific_name='plant 2',
                                      plant_type='plant type',
                                      date_added=date(2012, 05, 20))
    plant3 = family2.plant_set.create(scientific_name='plant 3',
                                      plant_type='plant type',
                                      date_added=date(2012, 05, 20))
    plant4 = family2.plant_set.create(scientific_name='plant 4',
                                      plant_type='plant type',
                                      date_added=date(2012, 05, 20))

    plant1.plantcommonname_set.create(common_name='plant1 cn1', primary=True)
    plant1.plantcommonname_set.create(common_name='plant1 cn2', primary=False)
    plant2.plantcommonname_set.create(common_name='plant2 cn1', primary=True)
    plant2.plantcommonname_set.create(common_name='plant2 cn2', primary=False)
    plant3.plantcommonname_set.create(common_name='plant3 cn1', primary=True)
    plant3.plantcommonname_set.create(common_name='plant3 cn2', primary=False)
    plant4.plantcommonname_set.create(common_name='plant4 cn1', primary=False)
    plant4.plantcommonname_set.create(common_name='plant4 cn2', primary=True)

    color1 = ColorRange.objects.create(
        color_range='red', icon_file_name='color_icon.jpg')
    color2 = ColorRange.objects.create(
        color_range='green', icon_file_name='color_icon.jpg')
    color3 = ColorRange.objects.create(
        color_range='blue', icon_file_name='color_icon.jpg')

    ImageInfo.objects.create(plant=plant1,
                             color_range=color1,
                             file_name='img1.jpg',
                             image_width=300,
                             image_height=200,
                             primary=True)

    ImageInfo.objects.create(plant=plant1,
                             color_range=color1,
                             file_name='img2.jpg',
                             image_width=300,
                             image_height=200,
                             primary=False)

    ImageInfo.objects.create(plant=plant2,
                             color_range=color1,
                             file_name='img3.jpg',
                             image_width=300,
                             image_height=200,
                             primary=True)

    ImageInfo.objects.create(plant=plant2,
                             color_range=color2,
                             file_name='img4.jpg',
                             image_width=300,
                             image_height=200,
                             primary=False)

    ImageInfo.objects.create(plant=plant3,
                             color_range=color3,
                             file_name='img5.jpg',
                             image_width=300,
                             image_height=200,
                             primary=False)

    ImageInfo.objects.create(plant=plant3,
                             color_range=color3,
                             file_name='img6.jpg',
                             image_width=300,
                             image_height=200,
                             primary=True)

    ImageInfo.objects.create(plant=plant4,
                             color_range=color3,
                             file_name='img7.jpg',
                             image_width=300,
                             image_height=200,
                             primary=True)

    ImageInfo.objects.create(plant=plant4,
                             color_range=color3,
                             file_name='img8.jpg',
                             image_width=300,
                             image_height=200,
                             primary=False)


class DatabaseTests(TestCase):
    def test_number_of_plant_entries(self):
        create_database()
        number_of_entries = Plant.objects.all().count()
        self.assertEqual(number_of_entries, 4)

    def test_number_of_plant_common_name_entries(self):
        create_database()
        number_of_entries = PlantCommonName.objects.all().count()
        self.assertEqual(number_of_entries, 8)

    def test_number_of_family_entries(self):
        create_database()
        number_of_entries = Family.objects.all().count()
        self.assertEqual(number_of_entries, 2)

    def test_number_of_family_common_name_entries(self):
        create_database()
        number_of_entries = FamilyCommonName.objects.all().count()
        self.assertEqual(number_of_entries, 4)

    def test_number_of_color_range_entries(self):
        create_database()
        number_of_entries = ColorRange.objects.all().count()
        self.assertEqual(number_of_entries, 3)

    def test_number_of_iamge_info_entries(self):
        create_database()
        number_of_entries = ImageInfo.objects.all().count()
        self.assertEqual(number_of_entries, 8)

    def test_query_plant_by_color_blue(self):
        create_database()
        cr_id = ColorRange.objects.filter(color_range='blue').get().id
        all_plants = Plant.objects.all()
        f1 = all_plants.filter(imageinfo__color_range_id=cr_id)
        number_of_entries = f1.count()
        self.assertEqual(number_of_entries, 4)

    def test_query_plant_by_color_green(self):
        create_database()
        cr_id = ColorRange.objects.filter(color_range='green').get().id
        all_plants = Plant.objects.all()
        f1 = all_plants.filter(imageinfo__color_range_id=cr_id)
        number_of_entries = f1.count()
        self.assertEqual(number_of_entries, 1)

    def test_query_plant_by_color_red(self):
        create_database()
        cr_id = ColorRange.objects.filter(color_range='red').get().id
        all_plants = Plant.objects.all()
        f1 = all_plants.filter(imageinfo__color_range_id=cr_id)
        number_of_entries = f1.count()
        self.assertEqual(number_of_entries, 3)

    def test_query_plant_show_only_primary_common_name(self):
        create_database()
        all_plants = Plant.objects.all()
        f1 = all_plants.filter(plantcommonname__primary=True)
        number_of_entries = f1.count()
        self.assertEqual(number_of_entries, 4)

    def test_query_plant_with_common_name(self):
        create_database()
        all_common_names = PlantCommonName.objects.all()
        p_type = all_common_names[0].plant.plant_type
        self.assertEqual(p_type, 'plant type')
        self.assertEqual(all_common_names.count(), 8)

    def test_query_plant_with_common_name_only_primary_image(self):
        create_database()
        all_common_names = PlantCommonName.objects.all()
        p_type = all_common_names[0].plant.plant_type
        self.assertEqual(p_type, 'plant type')
        self.assertEqual(all_common_names.count(), 8)

    def test_query_group_by_scientific_name_in_plant(self):
        create_database()
        cr_id = ColorRange.objects.filter(color_range='blue').get().id
        all_plants = Plant.objects.all()
        f1 = all_plants.filter(imageinfo__color_range_id=cr_id)
        f2 = f1.values('scientific_name').annotate(Count('scientific_name'))
        number_of_entries = f2.count()
        self.assertEqual(number_of_entries, 2)

    def test_query_plant_by_color_green_return_non_primary_image(self):
        create_database()
        cr_id = ColorRange.objects.filter(color_range='green').get().id
        f1 = Plant.objects.filter(imageinfo__color_range_id=cr_id).all()
        # f1 = all_plants[0].imageinfo_set.filter(color_range_id=cr_id).all()
        number_of_entries = f1.count()
        self.assertEqual(number_of_entries, 1)


class FamilyMethodTests(TestCase):
    def test_get_formatted_common_names_with_no_common_names(self):
        """
        formatted_common_names should be None if there are no common names.
        """
        family = Family.objects.create(scientific_name='family 1',
                                       icon_file_name='family_icon.jpg')
        self.assertEqual(family.formatted_common_names, None)

    def test_get_formatted_common_names_with_one_common_name(self):
        """
        formatted_common_names should be "some name" if there is
        only one common name.
        """
        family = Family.objects.create(scientific_name='family 1',
                                       icon_file_name='family_icon.jpg')
        family.familycommonname_set.create(common_name='some name')
        self.assertEqual(family.formatted_common_names, 'some name')

    def test_get_formatted_common_names_with_two_common_names(self):
        """
        formatted_common_names should be 'some name or some name'
        if there are two common names.
        """
        family = Family.objects.create(scientific_name='family 1',
                                       icon_file_name='family_icon.jpg')
        family.familycommonname_set.create(common_name='some name')
        family.familycommonname_set.create(common_name='some name')
        self.assertEqual(
            family.formatted_common_names, 'some name or some name')

    def test_get_formatted_common_names_with_more_than_two_common_names(self):
        """
        formatted_common_names should be 'some name, some name or some name'
        if there are more than two common names.
        """
        family = Family.objects.create(scientific_name='family 1',
                                       icon_file_name='family_icon.jpg')
        family.familycommonname_set.create(common_name='some name')
        family.familycommonname_set.create(common_name='some name')
        family.familycommonname_set.create(common_name='some name')
        self.assertEqual(family.formatted_common_names,
                         'some name, some name or some name')


class PlantMethodTests(TestCase):
    def test_get_formatted_common_names_with_no_common_names(self):
        """
        formatted_common_names should be None if there are no common names.
        """
        family = Family.objects.create(scientific_name='family 1',
                                       icon_file_name='family_icon.jpg')
        plant = family.plant_set.create(scientific_name='plant 1',
                                        plant_type='plant type',
                                        date_added=date(2012, 05, 20))
        self.assertEqual(plant.formatted_common_names, None)

    def test_get_formatted_common_names_with_one_common_name(self):
        """
        formatted_common_names should be 'primary name'
        if there is only one common name.
        """
        family = Family.objects.create(scientific_name='family 1',
                                       icon_file_name='family_icon.jpg')
        plant = family.plant_set.create(scientific_name='plant 1',
                                        plant_type='plant type',
                                        date_added=date(2012, 05, 20))
        plant.plantcommonname_set.create(
            common_name='primary name', primary=True)
        self.assertEqual(plant.formatted_common_names, 'primary name')

    def test_get_formatted_common_names_with_two_common_names(self):
        """
        formatted_common_names should be 'primary name or other name'
        if there are more than two common names.
        """
        family = Family.objects.create(scientific_name='family 1',
                                       icon_file_name='family_icon.jpg')
        plant = family.plant_set.create(scientific_name='plant 1',
                                        plant_type='plant type',
                                        date_added=date(2012, 05, 20))
        plant.plantcommonname_set.create(
            common_name='other name', primary=False)
        plant.plantcommonname_set.create(
            common_name='primary name', primary=True)
        self.assertEqual(
            plant.formatted_common_names, 'primary name or other name')

    def test_get_formatted_common_names_with_more_than_two_common_names(self):
        """
        formatted_common_names should be
        'primary name, other name or other name'
        if there are more than two common names.
        """
        family = Family.objects.create(scientific_name='family 1',
                                       icon_file_name='family_icon.jpg')
        plant = family.plant_set.create(scientific_name='plant 1',
                                        plant_type='plant type',
                                        date_added=date(2012, 05, 20))
        plant.plantcommonname_set.create(
            common_name='other name', primary=False)
        plant.plantcommonname_set.create(
            common_name='other name', primary=False)
        plant.plantcommonname_set.create(
            common_name='primary name', primary=True)
        self.assertEqual(plant.formatted_common_names,
                         'primary name, other name or other name')

    def test_get_primary_common_name(self):
        family = Family.objects.create(scientific_name='family 1',
                                       icon_file_name='family_icon.jpg')
        plant = family.plant_set.create(scientific_name='plant 1',
                                        plant_type='plant type',
                                        date_added=date(2012, 05, 20))
        plant.plantcommonname_set.create(
            common_name='other name', primary=False)
        plant.plantcommonname_set.create(
            common_name='primary name', primary=True)
        self.assertEqual(plant.primary_common_name, 'primary name')

    def test_get_primary_image_file_name(self):
        family = Family.objects.create(scientific_name='family 1',
                                       icon_file_name='family_icon.jpg')
        plant = family.plant_set.create(scientific_name='plant 1',
                                        plant_type='plant type',
                                        date_added=date(2012, 05, 20))
        color = ColorRange.objects.create(
            color_range='blue', icon_file_name='color_icon.jpg')

        ImageInfo.objects.create(plant=plant,
                                 color_range=color,
                                 file_name='img1.jpg',
                                 image_width=300,
                                 image_height=200,
                                 primary=False)
        ImageInfo.objects.create(plant=plant,
                                 color_range=color,
                                 file_name='img2.jpg',
                                 image_width=300,
                                 image_height=200,
                                 primary=True)
        self.assertEqual(plant.primary_image_file_name, 'img2.jpg')

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


class ByCommonNameViewTests(TestCase):
    def test_by_common_name_view_with_no_common_names(self):
        """
        If no plant common names exist, an appropriate message should be
        displayed.
        """
        response = self.client.get(
            reverse('webapp:wildflowers_by_common_name'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No plant common names are available.')
        self.assertQuerysetEqual(
            response.context['plant_common_name_list'], [])

    def test_by_common_name_view_with_valid_database(self):
        create_database()
        response = self.client.get(
            reverse('webapp:wildflowers_by_common_name'))
        self.assertQuerysetEqual(
            response.context['plant_common_name_list'],
            ['<PlantCommonName: plant1 cn1>',
             '<PlantCommonName: plant1 cn2>',
             '<PlantCommonName: plant2 cn1>',
             '<PlantCommonName: plant2 cn2>',
             '<PlantCommonName: plant3 cn1>',
             '<PlantCommonName: plant3 cn2>',
             '<PlantCommonName: plant4 cn1>',
             '<PlantCommonName: plant4 cn2>'])


class ByScientificNameViewTests(TestCase):
    def test_by_scientific_name_view_with_no_scientific_names(self):
        """
        If no plant scientific names exist, an appropriate message should be
        displayed.
        """
        response = self.client.get(
            reverse('webapp:wildflowers_by_scientific_name'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'No plant scientific names are available.')
        self.assertQuerysetEqual(
            response.context['plant_scientific_name_list'], [])

    def test_by_scientific_name_view_with_valid_database(self):
        create_database()
        response = self.client.get(
            reverse('webapp:wildflowers_by_scientific_name'))
        self.assertQuerysetEqual(
            response.context['plant_scientific_name_list'],
            ['<Plant: plant 1>',
             '<Plant: plant 2>',
             '<Plant: plant 3>',
             '<Plant: plant 4>'])


class ByFamilyViewTests(TestCase):
    def test_by_family_view_with_no_families(self):
        """
        If no families exist, an appropriate message should be
        displayed.
        """
        response = self.client.get(
            reverse('webapp:wildflowers_by_family'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'No families are available.')
        self.assertQuerysetEqual(
            response.context['family_list'], [])

    def test_by_family_view_with_valid_database(self):
        create_database()
        response = self.client.get(
            reverse('webapp:wildflowers_by_family'))
        self.assertQuerysetEqual(
            response.context['family_list'],
            ['<Family: family 1>',
             '<Family: family 2>'])


class ByColorRangeViewTests(TestCase):
    def test_by_color_range_view_with_no_color_ranges(self):
        """
        If no color rangess exist, an appropriate message should be
        displayed.
        """
        response = self.client.get(
            reverse('webapp:wildflowers_by_color_range'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'No color ranges are available.')
        self.assertQuerysetEqual(
            response.context['color_range_list'], [])

    def test_by_color_range_view_with_valid_database(self):
        create_database()
        response = self.client.get(
            reverse('webapp:wildflowers_by_color_range'))
        self.assertQuerysetEqual(
            response.context['color_range_list'],
            ['<ColorRange: blue>',
             '<ColorRange: green>',
             '<ColorRange: red>'])


class InFamilyViewTests(TestCase):
    def test_in_family_view_with_invalid_family_id(self):
        """
        The plants_in_family view of a family with invalid id should return
        a 404 not found.
        """
        random_id = random.randint(1, 100)
        response = self.client.get(
            reverse('webapp:wildflowers_family', args=(random_id,)))
        self.assertEqual(response.status_code, 404)

    def test_in_family_view_with_valid_family_id(self):
        create_database()
        family = Family.objects.all()[0]
        family_id = family.id
        response = self.client.get(
            reverse('webapp:wildflowers_family', args=(family_id,)))
        self.assertEqual(response.status_code, 200)


class InColorRangeViewTests(TestCase):
    def test_in_color_range_view_with_invalid_color_range_id(self):
        """
        The plants_in_color_range view of a family with invalid id should
        return a 404 not found.
        """
        random_id = random.randint(1, 100)
        response = self.client.get(
            reverse('webapp:wildflowers_color_range', args=(random_id,)))
        self.assertEqual(response.status_code, 404)

    def test_in_color_range_view_with_valid_family_id(self):
        create_database()
        color_range = Family.objects.all()[0]
        color_range_id = color_range.id
        response = self.client.get(
            reverse('webapp:wildflowers_color_range', args=(color_range_id,)))
        self.assertEqual(response.status_code, 200)


class PlantDetailViewTests(TestCase):
    def test_plant_detail_view_with_invalid_plant_id(self):
        """
        The plant detail view of a plant with invalid id should
        return a 404 not found.
        """
        random_id = random.randint(1, 100)
        response = self.client.get(
            reverse('webapp:wildflowers_detail', args=(random_id,)))
        self.assertEqual(response.status_code, 404)

    def test_plant_detail_view_with_valid_plant_id(self):
        create_database()
        plant = Plant.objects.all()[0]
        plant_id = plant.id
        response = self.client.get(
            reverse('webapp:wildflowers_detail', args=(plant_id,)))
        self.assertContains(response, plant.scientific_name, status_code=200)
