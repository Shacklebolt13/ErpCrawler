from django.urls import path
from . import views


urlpatterns = [
    path("getOrCreate", views.goc, name="goc"),
    path("updateUser", views.update, name="update"),
    path("practiceSubmit", views.practiceSubmit, name="psubmit"),
    path("sponsoredSubmit", views.sponsoredSubmit, name="ssubmit"),
    path("practiceLeaderboard", views.getLeaderBoard, name="pleaderboard"),
    path("sponsoredLeaderboard", views.sponsoredLeaderBoard, name="sleaderboard"),
    path("practiceQuestions", views.getQuestion, name="pquest"),
    path("sponsoredQuestions", views.getSponsoredQuestion, name="squest"),
    path("uploadQuestions", views.uploadQuestions, name="uploadQ"),
]
