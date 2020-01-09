from django.shortcuts import render, redirect
from django.views import generic

from django.views.generic import TemplateView

from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from .models import student, attendance_history
from datetime import datetime

# import bluetooth
# import sqlite3
# Create your views here.

def login(request):
    return render(request, 'login.html')


def student_table(request):
    if request.method == 'POST':
        sroll = request.POST['fullname']
        print(sroll)
    srecords = attendance_history.objects.filter(roll_no=sroll)
    if len(srecords) > 0:

        return render(request, 'student_table.html', { 'srecords': srecords})
    else:
        messages.info(request,'No attendance log.')         
        return render(request, 'login.html')




def home(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User = auth.authenticate(username=username ,password=password )
        
        if User is not None:
            auth.login(request, User)
            return render(request,'home.html')
        else:
            messages.info(request,'Invalid credentials.') 
            return render(request,'login.html')  
    else:
        return render(request,'login.html')    

def blue(request):
    '''conn = sqlite3.connect('db.sqlite3')

    dis_mac = bluetooth.discover_devices(duration=8, lookup_names=True,
                                            flush_cache=True, lookup_class=False)
    db_mac = conn.execute("SELECT mac_address from info_student")

    for item_db_mac in db_mac:
        print('\n')
        for item in dis_mac:
            if item[0] == item_db_mac[0]:
                conn.execute("UPDATE info_student SET attendence_stat = 1 where mac_address='{}'".format(item_db_mac[0]))
                conn.commit()
            
                break;

    conn.close()'''
    brecords = student.objects.all()
    for i in brecords:
        if i.attendence_stat == True:
            a = attendance_history(student = i.full_name, roll_no = i.roll_no, datetime=datetime.now(), attendance=i.attendence_stat)
            a.save()
            i.attendence_stat = False
            i.save()
    return render(request, 'home.html')





def about(request):
    return render(request, 'about.html')

def refresh(request): 
    records = student.objects.all()
    for i in records:
        if i.attendence_stat == True:
            a = attendance_history(student = i.full_name, roll_no = i.roll_no, datetime=datetime.now(), attendance=i.attendence_stat)
            a.save()
            i.attendence_stat = False
            i.save()
    return render(request, 'home.html')
    

def attendance(request):
    att_list = attendance_history.objects.all()
    # print(att_list)
    args = { 'att_list': att_list}
    return render(request, 'attendance.html', args)








# def count(request): 
#     records = attendance_history.objects.all()
#     count=0
#     for i in records:
#         for j in records:
#             if i.full_name == j.full_name:
#                 count= count + 1

#     return render(request, 'home.html')    