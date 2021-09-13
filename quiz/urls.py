from django.urls import path
from . import views



urlpatterns = [
    path('getOrCreate',views.goc,name='goc'),
    path('updateUser',views.update,name='update'),
    path('practiceSubmit',views.practiceSubmit,name='psubmit'),
    path('practiceLeaderboard',views.getLeaderBoard,name='pleaderboard'),
    path('practiceQuestions',views.getQuestion,name='pquest'),
    ]
