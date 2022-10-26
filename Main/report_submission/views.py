from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import *
from .models import Patient_Report
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, authenticate


# Create your views here.
def home(request):
    return render(request, 'home.html')

def doctor_view_all_reports(request):
    if request.method == 'GET':
        reports = Patient_Report.objects.all()
        return render(request, 'view-all-reports.html',context= {'reports': reports})

def submit_report(request):
	if request.method == 'POST':
		form = PatientForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()
			return redirect('success')
	else:
		form = PatientForm()
	return render(request, 'report-submit.html', {'form' : form})


def success(request):
	return HttpResponse('successfully uploaded')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("all_reports")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

import tensorflow as tf
import numpy as np
import cv2
import os
import pandas as pd

data = pd.read_csv("trainLabels.csv")
model = tf.keras.models.load_model("model-mobile-net.h5")
image_location = './media/'
files = os.listdir(image_location)
class_list = ['No_DR', 'Mild_DR', 'Moderate_DR', 'Severe_DR', 'Proliferative_DR']
def make_prediction(img_path,rt):
	a_file = os.path.join(image_location, img_path)
	img = cv2.imread(a_file)
	img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img=cv2.resize(img, (300,300))
	# img=img/255.0
	img=np.expand_dims(img, axis=0)
	prediction =model.predict (img, batch_size=1, verbose=0)
	pred=np.argmax(prediction)
	return rt+ ' retina the predicted class is '+ class_list[pred]+ ' with a probability of '+ str(prediction[0][pred])
# print(a_file)
def generate_report(request):
    if request.method == "GET":
        left_img = request.GET['left_img']
        right_img = request.GET['right_img']
        # parts = left_img.split("/")
        # file_name = parts[-1].split(".")
        # rev = file_name[0][::-1]
        # print(rev)
        # count = 0
        # for i in rev:
        #     if i == "_":
        #         print(count)
        #         break
        #     count += 1
        # f = file_name[0][0:len(file_name[0])-count-1]
        # # print(data[f])
        left_message = make_prediction(left_img,"Left") 
        right_message = make_prediction(right_img,"Right")
        print(left_img)
        print(right_img)
        dic = {"left_message" : left_message, "right_message" : right_message}
        print(dic)
        return JsonResponse(dic)
    



