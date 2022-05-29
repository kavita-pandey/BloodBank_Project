from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import NeedBlood
from .models import DonateBlood
from .models import Blood_Bank
from .models import fact
from .models import Blood_Camps
from .models import chart
import re

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def index(request):
    a=fact.objects.all()
    return render(request,'index.html', {'a':a})

def donateblood(request):
    return render(request,'donateblood.html')

def needblood(request):
    return render(request,'needblood.html')

def aboutus(request):
    return render(request,'aboutus.html')

def facts(request):
    a=fact.objects.all()
    return render(request,'facts.html',{'a':a})

def donorfitnesschart(request):
    a=chart.objects.all()
    return render(request,'donorfitnesschart.html',{'a':a})

def searchbloodbanks(request):
    a=Blood_Bank.objects.all()
    return render(request,'searchbloodbanks.html',{'a':a})

def searchbloodcamps(request):
    a=Blood_Camps.objects.all()
    return render(request,'searchbloodcamps.html',{'a':a})

def predict(request):
    return render(request, 'predict.html')

def result(request):
    data=pd.read_csv(r"D:\Kavita_MajorProject\Django_blood_bank-master\dataset\diabetes.csv")
    X=data.drop("Outcome", axis=1)
    Y=data['Outcome']
    X_train, X_test, Y_train, Y_test=train_test_split(X,Y,test_size=0.30)
    model=LogisticRegression(solver='lbfgs',class_weight='balanced', max_iter=10000)
    model.fit(X_train, Y_train)

    val1=float(request.GET['n1'])
    val2=float(request.GET['n2'])
    val3=float(request.GET['n3'])
    val4=float(request.GET['n4'])
    val5=float(request.GET['n5'])
    val6=float(request.GET['n6'])
    val7=float(request.GET['n7'])
    val8=float(request.GET['n8'])
    
    pred=model.predict([[val1, val2, val3, val4, val5, val6, val7, val8]])
    print(pred)
    result2=""
    if pred==[1]:
        result2="Health is good you can donate"
    else:
        result2="You can't donate...!"


    return render(request, 'predict.html', {"result2":result2, "pred":pred})



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        ff=0
        while True:   
            if not re.search("[@]", email): 
                messages.info(request,'Not a valid Email-id')
                ff=-1
                return redirect('register')
                break
            else:
                ff=0
                break
        
        password = password1
        flag = 0
        while True:   
            if (len(password)<8): 
                flag = -1
                messages.info(request,'Password length must be at least 8 characters.NOTE: Password must contain at least one capital alphabet,special character and numeric digit.')
                return redirect('register')
                break
            elif not re.search("[A-Z]", password): 
                flag = -1
                messages.info(request,'Password must contain atleast one capital alphabet.NOTE:Password must contain at least one capital alphabet,special character and numeric digit.')
                return redirect('register')
                break
            elif not re.search("[0-9]", password): 
                flag = -1
                messages.info(request,'Password must contain atleast one numeric digit. NOTE:Password must contain at least one capital alphabet,special character and numeric digit.')
                return redirect('register')
                break
            elif not re.search("[!@#$%^&*()_]", password): 
                flag = -1
                messages.info(request,'Password must contain atleast one special character.Password must contain at least one capital alphabet,special character and numeric digit.')
                return redirect('register')
                break
            elif re.search("\s", password): 
                flag = -1
                break
            else: 
                flag = 0
                break
  
        if password1==password2 and flag == 0 and ff==0:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already registered')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1 , email=email, first_name=first_name, last_name=last_name)
                user.save()
                print("usr don")
                return redirect('login')
        else:
            messages.info(request,'Password not matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request,'register.html')


def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def need(request):
    print('form submitted')
    city=request.POST['city']
    requestname=request.POST['requestname']
    contact=request.POST['contact']
    blood_group=request.POST['blood_group']

    needer = NeedBlood(blood_group=blood_group,requestname=requestname,city=city,contact=contact)
    needer.save();
    return render(request,'index.html')

def donate(request):
    print('form submitted')
    city=request.POST['city']
    donorname=request.POST['donorname']
    contact=request.POST['contact']
    blood_group=request.POST['blood_group']

    needer = DonateBlood(blood_group=blood_group,donorname=donorname,city=city,contact=contact)
    needer.save();
    return render(request,'index.html')

def temp(request):
    a=DonateBlood.objects.filter.all()
    return render(request,'temp.html',{'a':a})

def requestlist(request):
    return render(request,'requestlist.html')

def donorlist(request):
    return render(request,'donorlist.html',)


def don(request):
    c=request.POST['blood_group']
    b=request.POST['city']
    a=DonateBlood.objects.filter(blood_group=c,city=b)
    return render(request,'donorlist.html',{'a':a})

def req(request):
    c=request.POST['blood_group']
    b=request.POST['city']
    a=NeedBlood.objects.filter(blood_group=c,city=b)
    return render(request,'requestlist.html',{'a':a})

def citydonar(request):
    return render(request,'citydonar.html')

def nearestpatient(request):
    return render(request,'nearestpatient.html')

def donationmanual(request):
    return render(request,'donationmanual.html')