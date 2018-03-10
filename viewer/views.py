# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from viewer.forms import PlayListForm


def landing(request):
    ctx = {}
    ctx['form'] = PlayListForm()

    return render(request, 'landing.html', context=ctx)
