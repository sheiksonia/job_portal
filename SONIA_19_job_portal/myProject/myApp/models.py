from django.db import models
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):
    
    USER=[
        ('recruiter','Recruiter'),
        ('seeker','Seeker'),
    ]
    user_type=models.CharField(choices=USER,max_length=100,null=True)
    Profile_Pic=models.ImageField(upload_to='Media/Profile_Pic',null=True)
    contact_no=models.CharField(max_length=100,null=True)
    
    def __str__(self):   
        
        return f"{self.username}"
    
class seekerProfileModel(models.Model):
    SKILLS=[
        ('Python','Python'),
        ('Java','Java'),
        ('C++','C++'),
        ('Data Science','Data Science'),
        ('Machine Learning','Machine Learning'),
    ]
    
    user=models.OneToOneField(customUser,on_delete=models.CASCADE,related_name='seekerProfile')
    skills=models.CharField(max_length=100,choices=SKILLS,null=True)
   
    def __str__(self):
        return f"{self.user.username}"
    
    
class recruiterProfileModel(models.Model):
    
   
    user = models.OneToOneField(customUser, on_delete=models.CASCADE,related_name='recruiterProfile')
   
    def __str__(self):
        return f"{self.user.username}"
    
    
class JobModel(models.Model):
    SKILLS=[
        ('Python','Python'),
        ('Java','Java'),
        ('C++','C++'),
        ('Data Science','Data Science'),
        ('Machine Learning','Machine Learning'),
    ]
    user = models.ForeignKey(customUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    openings = models.TextField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    vancancy = models.CharField(max_length=100)
    skills=models.CharField(max_length=100,choices=SKILLS,null=True)
    job_Pic=models.ImageField(upload_to='Media/Profile_Pic',null=True)
    
    def __str__(self):
        return f"{self.user.username} {self.title}"
    
class jobApplyModel(models.Model):

    user=models.ForeignKey(customUser,on_delete=models.CASCADE,null=True)
    job=models.ForeignKey(JobModel,on_delete=models.CASCADE,null=True)
    Resume = models.FileField(upload_to="Media/Resume",max_length=200, null=True, blank=True) 
    Cover = models.TextField(null=True, blank=True) 
    Skills = models.CharField(max_length=200, null=True, blank=True) 
    Apply_Image=models.ImageField(upload_to='Media/Apply_Image',null=True)
    
    def __str__(self) -> str:
        return self.user.username+"-"+self.job.title       
    
  