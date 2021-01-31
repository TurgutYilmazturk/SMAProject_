from django.urls import path
from . import views

app_name='analysis'

urlpatterns=[
    path('',views.AnalysisView.as_view(),name='analysis_home'),
    path('history/',views.HistoryView.as_view(),name='history'),

]
