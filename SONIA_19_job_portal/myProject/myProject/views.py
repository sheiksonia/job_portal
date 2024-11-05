from django.shortcuts import render,redirect

from myApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def signupPage(request):
    
    if request.method=='POST':
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        Confirm_password=request.POST.get("Confirm_password")
        user_type=request.POST.get("user_type")
        Profile_Pic=request.FILES.get("Profile_Pic")
    
        
        if password==Confirm_password:
            
            
            user=customUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                Profile_Pic=Profile_Pic,
            )
            if user_type=='seeker':
                seekerProfileModel.objects.create(user=user)
                
            elif user_type=='recruiter':
                recruiterProfileModel.objects.create(user=user)
            
            return redirect("signInPage")
            
    return render(request,"signupPage.html")


def signInPage(request):
    if request.method == 'POST':
        
        user_name=request.POST.get("username")
        pass_word=request.POST.get("password")

        try:
            user = authenticate(request, username=user_name, password=pass_word)

            if user is not None:
                login(request, user)
                return redirect('homePage') 
            else:
                return redirect('signInPage')

        except customUser.DoesNotExist:
            return redirect('signInPage')

    return render(request, 'signInPage.html')

@login_required
def homePage(request):
    
    
    return render(request,"homePage.html")


def logoutPage(request):
    
    logout(request)
    
    return redirect('signInPage')

@login_required
def profilePage(request):
    
    return render(request,"profilePage.html")


def addJobPage(request):
    current_user=request.user
    
    if current_user.user_type == "recruiter":
     if request.method== 'POST':
        title=request.POST.get('title')
        openings=request.POST.get('openings')
        category=request.POST.get('category')
        description=request.POST.get('description')
        vancancy=request.POST.get('vacancy')
        job_Pic=request.FILES.get('Job_Image')
        jobs = JobModel(user=current_user,
        title=title,
        openings=openings,
        category=category,
        description =description,
        vancancy=vancancy,
        job_Pic=job_Pic,    
        )
        jobs.save()
        return redirect("createdJob")
    return render(request,'addjob.html')
    

def createdJob(request):
    
    current_user=request.user
    
    job=JobModel.objects.filter(user=current_user)
    
    context={
        "Jobs":job
    }
    return render(request,"createdJob.html",context)


def deleteJob(request,myid):
    data = JobModel.objects.get(id=myid)
    data.delete()
    return redirect('createdJob')

@login_required
def editpage(req,id):
    Job=JobModel.objects.get(id=id)
    return render(req,"editjob.html",{'Jobs':Job})

def updatepage(request):
   current_user=request.user
   if current_user.user_type == "recruiter":
    if request.method== 'POST':
        stuid=request.POST.get('id')
        title=request.POST.get('title')
        openings=request.POST.get('openings')
        category=request.POST.get('category')
        description=request.POST.get('description')
        vancancy=request.POST.get('vacancy')
        job_Pic=request.FILES.get('Job_Image')
        jobs = JobModel(user=current_user,
        id= stuid,                
        title=title,
        openings=openings,
        category=category,
        description =description,
        vancancy=vancancy,
        job_Pic=job_Pic,    
        )
        jobs.save()
        return redirect("createdJob")
    
    
def applyJob(request,job_id):
    
    jobs=JobModel.objects.get(id=job_id)
    context={
        'jobs':jobs,
        'applyJob':jobs
    }
    
    
    if request.method=='POST':
        
        Skills=request.POST.get("skill")
        Cover=request.POST.get("Cover")
        Apply_Image=request.FILES.get("apply_Image")
        Resume=request.FILES.get("resume")
        
        apply=jobApplyModel(
            user=request.user,
            job=jobs,
            Skills=Skills,
            Cover=Cover,
            Resume=Resume,
            Apply_Image=Apply_Image,
        )
        
        apply.save()
        
        return redirect("jobapplied")
        
    return render(request,"applyJob.html",context) 


def searchJob(request):
    
    query = request.GET.get('query')
    
    jobs = JobModel.objects.filter(Q(title__icontains=query) 
                                       |Q(category__icontains=query)
                                       |Q(skills__icontains=query)) 
    
    
    
    context={
        'query':query,
        'jobs':jobs
    }
    
    return render(request,"search.html",context)  

def jobFeed(request):
    
    jobs=JobModel.objects.all()
    context={
        'jobs':jobs,
        
    }
    
    return render(request,"jobFeed.html",context)


def skillMaching(request):
    user=request.user
    myskill=user.seekerProfile.skills
    jobs=JobModel.objects.filter(skills=myskill)
    context={
        'jobs':jobs
    }
    return render(request,"skillMaching.html",context) 

 

def jobapplied(req):
    
    jobs=jobApplyModel.objects.all()
    context={
        
        "applyJob":jobs
    }
    return render(req,"applidjob.html",context)

def viewJOb(request,job_id):

    jobs=JobModel.objects.filter(id=job_id)

    context= {
        'jobs': jobs
    }
    
    
    return render(request,"singleview.html",context)

@login_required
def editProfilePage(request):
    
    
    
    current_user=request.user
    
    if request.method=='POST':
        current_user.username=request.POST.get("username")
        current_user.first_name=request.POST.get("first_name")
        current_user.last_name=request.POST.get("last_name")
        current_user.email=request.POST.get("email")
        current_user.job_id=request.POST.get("job_id")
        skill = request.POST.get('skills')
        if request.FILES.get("profile_pic"):
            current_user.Profile_Pic=request.FILES.get("profile_pic")
        
    
            
        try:
            seekerProfile=seekerProfileModel.objects.get(user=current_user)
            seekerProfile.skills = skill
            seekerProfile.save()
            current_user.save()
            
            return redirect("profilePage")
            
        except seekerProfileModel.DoesNotExist:
            seekerProfile=None
            
        try:
            recruiterProfile=recruiterProfileModel.objects.get(user=current_user)
            
            recruiterProfile.Company_name=request.POST.get("Company_name")
            recruiterProfile.save()
            current_user.save()
            
            return redirect("profilePage")
            
        except recruiterProfileModel.DoesNotExist:
            recruiterProfile=None
    
    return render(request, "editprofile.html")              
    
    
    
   
    


   
    
    
    



