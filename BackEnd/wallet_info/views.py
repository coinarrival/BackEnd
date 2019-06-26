from django.shortcuts import render
from django.shortcuts import *
from django.http import *
from django.shortcuts import *
from django.urls import *
import traceback
import json
from .models import *
from django.db.utils import IntegrityError
from django.db.models import F
from .crypto import *
import math

MAX_PAGE_ITEMS = 6

def dealResponse(status_code, res_text={}):
    traceback.print_exc()
    dic = {
        400 : 'Decode Failed',
        406 : 'Verification Failed',
        200 : 'Standard Successed',
        201 : 'Create Resource Successed',
        409 : 'Confict Field or MultipleAcceptance', 
        500 : 'Unknown Server Error',
        404 : 'Not Exist', 
        416 : 'OutOfRange or CompletedTask', 
        401 : 'Unauthorized', 
        403 : 'TaskBeenFinished'
    }
    traceback.print_exc()
    print('[+] ' + dic[status_code])
    res_text['status_code'] = status_code
    resp = HttpResponse(encrypt(json.dumps(res_text)))
    # resp.status_code = status_code
    return resp

# Create your views here.
def get_balance(request):
    try:
        tusername = decrypt(request.GET['username'])
    except:
        return dealResponse(400)
    try:
        result = User.objects.get(username=tusername)
    except User.DoesNotExist:
        return dealResponse(404)
    return dealResponse(200, {'data':{'balance':result.wallet_set.first().balance}})