from django.shortcuts import render, get_list_or_404
from django.views import generic
from django.db.models import Count
from .models import Family, FamilyCommonName, ImageInfo
from .models import ColorRange, Plant, PlantCommonName

# Create your views here.


class ByCommonNameView(generic.ListView):
    template_name = 'webapp/by_common_name.html'
    context_object_name = 'plant_common_name_list'

    def get_queryset(self):
        """Return all plant common names"""
        return (PlantCommonName.objects.all()
                .filter(plant__imageinfo__primary=True)
                .order_by('common_name'))


class ByScientificNameView(generic.ListView):
    template_name = 'webapp/by_scientific_name.html'
    context_object_name = 'plant_scientific_name_list'

    def get_queryset(self):
        """Return all plant scientific names"""
        return Plant.objects.all().order_by('scientific_name')


class ByFamilyView(generic.ListView):
    template_name = 'webapp/by_family.html'
    context_object_name = 'family_list'

    def get_queryset(self):
        """Return all plant families"""
        return Family.objects.all().order_by('scientific_name')


class ByColorRangeView(generic.ListView):
    template_name = 'webapp/by_color_range.html'
    context_object_name = 'color_range_list'

    def get_queryset(self):
        """Return all plant color_ranges"""
        return ColorRange.objects.all().order_by('color_range')


class InFamilyView(generic.ListView):
    template_name = 'webapp/in_family.html'
    context_object_name = 'plants_in_family_list'

    def get_queryset(self):
        """Return all plants in a family"""
        f_id = self.kwargs['pk']
        q_set = Plant.objects.filter(
            family_id=f_id).order_by('scientific_name')
        plant_list = get_list_or_404(q_set)
        return plant_list


class InColorRangeView(generic.ListView):
    template_name = 'webapp/in_color_range.html'
    context_object_name = 'plants_in_color_range_list'

    def get_queryset(self):
        """Return all plants in a color_ranges"""
        cr_id = self.kwargs['pk']
        q_set = (Plant.objects
                 .filter(imageinfo__color_range_id=cr_id)
                 .order_by('scientific_name')
                 .annotate(Count('scientific_name')))
        plant_list = get_list_or_404(q_set)
        print plant_list[0]
        return plant_list


class PlantDetailView(generic.DetailView):
    model = Plant
    template_name = 'webapp/plant_detail.html'


def index(request):
    return render(request, 'webapp/index.html')


def references(request):
    return render(request, 'webapp/references.html')


def about_us(request):
    return render(request, 'webapp/about_us.html')
