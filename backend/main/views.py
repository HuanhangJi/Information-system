from django.shortcuts import render
from django.shortcuts import render
import json
from django.db.models import Q
from django.http import *
import numpy as np
import requests
import json
from .models import *
import hashlib


## TODO 主页
def index(request):
    return HttpResponse('主页')