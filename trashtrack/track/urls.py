from django.urls import path
from . import views
urlpatterns=[
    path('',views.main,name='main'),
    path('login/',views.loggin,name='login'),
    path('signup/',views.signup,name='signup'),
    path('NULL/',views.null,name='null'),
    path('Coimbature/',views.Coimbature,name='Coimbature'),
    path('Coimbature/pollachi/',views.pollachi,name='pollachi'),
    path('Coimbature/pollachi/kinathukadavu',views.kinathukadavu,name='kinathukadavu'),
]