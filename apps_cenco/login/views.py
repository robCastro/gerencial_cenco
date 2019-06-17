# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


# Create your views here.

def principal(request):
    if request.user.is_authenticated:
        if has_group(request.user, 'Director'):
            return redirect('ingreso_retiros_estudiantes')

        elif has_group(request.user, 'Profesor'):
            return redirect('')

        elif has_group(request.user, 'Supervisor'):
            return redirect('')

    else:
        return redirect('login')


def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

