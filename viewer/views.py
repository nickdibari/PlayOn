# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def landing(request):
    return render(request, 'landing.html')
