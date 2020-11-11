from django.urls import path, re_path
from .views import (
    ModuleListView,
    ModuleDetailView,
    ModuleCreateView,
    ModuleUpdateView,
    StudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentUpdateView,
    StudentMarkListView,
    StudentMarkDetailView,
    StudentMarkCreateView,
    StudentMarkUpdateView,
    StudentMarkDeleteView
)

urlpatterns = [
    re_path(r'^$', ModuleListView.as_view(), name='module-home'),
    re_path(r'^module/new/$', ModuleCreateView.as_view(), name='module-create'),
    re_path(r'^module/(?P<pk>\w{7})/$', ModuleDetailView.as_view(), name='module-details'),
    re_path(r'^module/(?P<pk>\w{7})/update/$', ModuleUpdateView.as_view(), name='module-update'),
    re_path(r'^results/(?P<module_code>\w{7})/(?P<year>\w{4})/$', StudentMarkListView.as_view(), name='results-home'),
    re_path(r'^results/(?P<module_code>\w{7})/(?P<year>\w{4})/new/$', StudentMarkCreateView.as_view(), name='results-create'),
    re_path(r'^results/(?P<module_code>\w{7})/(?P<year>\w{4})/(?P<student_id>\d{7})/(?P<pk>\d+)/$', StudentMarkDetailView.as_view(), name='results-details'),
    re_path(r'^results/(?P<module_code>\w{7})/(?P<year>\w{4})/(?P<student_id>\d{7})/(?P<pk>\d+)/update/$', StudentMarkUpdateView.as_view(), name='results-update'),
    re_path(r'^results/(?P<module_code>\w{7})/(?P<year>\w{4})/(?P<student_id>\d{7})/(?P<pk>\d+)/delete/$', StudentMarkDeleteView.as_view(), name='results-delete'),
    re_path(r'^student/$', StudentListView.as_view(), name='student-home'),
    re_path(r'^student/new/$', StudentCreateView.as_view(), name='student-create'),
    re_path(r'^student/(?P<pk>\d{7})/$', StudentDetailView.as_view(), name='student-details'),
    re_path(r'^student/(?P<pk>\d{7})/update/$', StudentUpdateView.as_view(), name='student-update'),
]
