from django.urls import path
from .views import SkillView, JobView

urlpatterns = [
    # post/
    path('', SkillView.as_view()),
    path('job', JobView.as_view()),
]
