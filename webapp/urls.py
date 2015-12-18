from django.conf.urls import url

from . import views

app_name = 'webapp'
urlpatterns = [
    # ex: /wildflowers/
    url(r'^$', views.index, name='wildflowers_index'),
    # ex: /wildflowers/references/
    url(r'^refernces/$', views.references, name='wildflowers_references'),
    # ex: /wildflowers/about_us?
    url(r'^about_us/$', views.about_us, name='wildflowers_about_us'),
    # ex: /wildflowers/by_common_name/
    url(r'^by_common_name/$',
        views.ByCommonNameView.as_view(),
        name='wildflowers_by_common_name'),
    # ex: /wildflowers/by_scientific_name/
    url(r'^by_scientific_name/$',
        views.ByScientificNameView.as_view(),
        name='wildflowers_by_scientific_name'),
    # ex: /wildflowers/by_family/
    url(r'^by_family/$',
        views.ByFamilyView.as_view(),
        name='wildflowers_by_family'),
    # ex: /wildflowers/by_color_range/
    url(r'^by_color_range/$',
        views.ByColorRangeView.as_view(),
        name='wildflowers_by_color_range'),
    # ex: /wildflowers/family/34/
    url(r'^family/(?P<pk>[0-9]+)/$',
        views.InFamilyView.as_view(),
        name='wildflowers_family'),
    # ex: /wildflowers/color_range/3/
    url(r'^color_range/(?P<pk>[0-9]+)/$',
        views.InColorRangeView.as_view(),
        name='wildflowers_color_range'),
    # ex: /wildflowers/detail/45/
    url(r'^detail/(?P<pk>[0-9]+)/$',
        views.PlantDetailView.as_view(),
        name='wildflowers_detail'),
]
