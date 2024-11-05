from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from myProject.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',signupPage,name="signupPage"),
    path("signInPage/", signInPage, name="signInPage"),
    path("homePage/", homePage, name="homePage"),
    path("logoutPage/", logoutPage, name="logoutPage"),
    path("ProfilePage/", profilePage, name="profilePage"),
    path("addJob/", addJobPage, name="addJob"),
    path("createdJob/", createdJob, name="createdJob"),
    path("deleteJob/<str:myid>", deleteJob, name="deleteJob"),
    path('editpage/<int:id>',editpage,name='editpage'),
    path('updatepage/', updatepage,name='updatepage'),
    path("searchJob/", searchJob, name="searchJob"),
    path("applyJob/<str:job_id>", applyJob, name="applyJob"),
    path("jobFeed/", jobFeed, name="jobFeed"),
    path("jobFeskillMachinged/", skillMaching, name="skillMaching"),
    path("applidjob/", jobapplied, name="jobapplied"),
    path("viewJOb/<str:job_id>", viewJOb, name="viewJOb"),
    path("editprofile/", editProfilePage, name="editprofile"),
    
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
