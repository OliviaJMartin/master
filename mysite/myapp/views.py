from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from time import gmtime, strftime
import datetime


class Overview(View):
    template = 'Overview.html'

    def get(self, request):
        la1 = MachineStatus.objects.filter(machineID='1').latest('id')
        la2 = MachineStatus.objects.filter(machineID='2').latest('id')
        la4 = MachineStatus.objects.filter(machineID='3').latest('id')
        ct = MachineStatus.objects.filter(machineID='4').latest('id')
        brachy = MachineStatus.objects.filter(machineID='5').latest('id')

        return render(request, self.template,
                      context={
                          'LA1_status': la1.Status,
                          'LA2_status': la2.Status,
                          'LA4_status': la4.Status,
                          'CT_status': ct.Status,
                          'Brachy_status': brachy.Status,

                          'LA1_user': la1.startUserID,
                          'LA2_user': la2.startUserID,
                          'LA4_user': la4.startUserID,
                          'CT_user': ct.startUserID,
                          'Brachy_user': brachy.startUserID,

                          'LA1_time': la1.startTime,
                          'LA2_time': la2.startTime,
                          'LA4_time': la4.startTime,
                          'CT_time': ct.startTime,
                          'Brachy_time': brachy.startTime,
                      },
                      )


class LoggingIn(View):
    template = 'Login.html'

    def get(self, request, machine):
        form = AuthenticationForm()
        request.session['machineChosen'] = machine
        return render(request, self.template, context={
            'form': form,
            'Machine_Name': machine,
        }, )

    def post(self, request, machine):
        request.session['machineChosen'] = machine
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['currentUsersName'] = user.first_name + ' ' + user.last_name
            request.session['currentUsersUsername'] = user.username
            return HttpResponseRedirect('/machinestatus/')
        else:
            return HttpResponseRedirect('/overview/')


class Status(LoginRequiredMixin, View):
    template = 'MachineStatus.html'
    login_url = '/login/'


    def get(self, request):
        machine = request.session.get("machineChosen")

        # database calls
        machine_info = MachineInfo.objects.get(name=machine)
        all_rows = MachineStatus.objects.filter(machineID=machine_info.id)
        most_recent = MachineStatus.objects.filter(machineID=machine_info.id).latest('id')

        reversed_array = reversed(all_rows)

        if machine == 'LA1':
            statusUser = request.session.get("LA1_currentUser")

        elif machine == 'LA2':
            statusUser = request.session.get("LA2_currentUser")

        elif machine == 'LA3':
            statusUser = request.session.get("LA4_currentUser")

        elif machine == 'CT':
            statusUser = request.session.get("CT_currentUser")

        else:
            statusUser = request.session.get("Brachytherapy_currentUser")

        currentStatus = most_recent.Status
        statusTime = most_recent.startTime

        return render(request, self.template, context={
            'Machine_Name': machine,
            'Serial_No': machine_info.serialNum,
            'SW_Version': machine_info.swVersion,
            'Machine_Status': currentStatus,
            'Current_Owner': most_recent.startUserID,
            'Start_Time': statusTime,
            'all_rows': reversed_array,
        }, )


class LoggingOut(View):
    def get(self, request):  # needs a self.variable to be allowed
        logout(request)
        return HttpResponseRedirect('/')


class Update(View):
    template = 'UpdateStatus.html'
    time = str(datetime.datetime.now())[0:19]
    # str(strftime("%d-%m-%Y %H:%M:%S", gmtime()))

    def get(self, request):
        currentUsersName = request.session.get('currentUsersName')
        machine = request.session.get("machineChosen")
        return render(request, self.template, context={
            'Machine_Name': machine,
            'User': currentUsersName,
        }, )

    def post(self, request):
        machine_chosen = request.session.get("machineChosen")
        status_submitted = request.POST['status']
        if status_submitted == 'Select status':
            return HttpResponseRedirect('/updatestatus/')

        description = request.POST['description']
        comments = request.POST['multiLineInput']
        username = request.session.get('currentUsersUsername')

        ms = MachineStatus(machineID=MachineInfo.objects.get(name=machine_chosen),
                           Status=status_submitted,
                           startUserID=AuthUser.objects.get(username=username),
                           startTime=self.time,
                           description=description,
                           comments=comments)
        ms.save()
        return HttpResponseRedirect('/machinestatus/')
