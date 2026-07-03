from django.urls import path
from . import views
from . import transcript_views

urlpatterns = [
    ## upload a transcript PDF and get back extracted subjects/marks
    path('upload_transcript/', transcript_views.upload_transcript),
    ## simple browser page to test the upload locally
    path('upload_test/', transcript_views.upload_test_page),
    ## find all the region subjects and return back subject and grade type
    path('search_subjects_by_region_abbreviation/', views.select_subject_by_region),
    ## count the final atar mark
    path('get_atar/',views.select_subjects_and_grades),

    path('get_grade_type_description/',views.get_grade_type_decription,name = 'get_grade_type_description')

]
