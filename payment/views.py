from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

import datetime

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse

from account.models import User
from complex.models import Complex, Session
from payment.models import Reserve, Payment
import requests
from django.conf import settings
import json

# Create your views here.
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8080/reserve/verify/'


@login_required
def reserve(request, session_id):
    if request.method == 'GET':
        session = get_object_or_404(Session, id=session_id)
        complex_instead = get_object_or_404(Complex, id=session.complex.id)
        context = {
            'session': session,
            'complex': complex_instead,
        }
        return render(request, 'payment/reserve.html', context=context)
    elif request.method == 'POST':
        session = get_object_or_404(Session, id=session_id)
        session.is_reserved = True
        session.save()
        reserved = Reserve()
        current_user = request.user
        reserved.user = get_object_or_404(User, id=current_user.id)
        reserved.session = get_object_or_404(Session, id=session_id)
        reserved.first_name = request.POST['first_name']
        reserved.last_name = request.POST['last_name']
        reserved.phone = request.POST['phone']
        reserved.reserve_note = request.POST['reserve_note']
        reserved.reserve_total = reserved.session.session_price
        reserved.ip = request.META.get("REMOTE_ADDR")
        yr = int(datetime.date.today().strftime("%Y"))
        dt = int(datetime.date.today().strftime("%d"))
        mt = int(datetime.date.today().strftime("%m"))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        reserve_number = current_date + str(reserved.id)
        reserved.reserve_number = reserve_number
        reserved.save()
        return redirect(reverse('account:dashboard',
                                kwargs={'phone': reserved.user.phone_number}))
    else:
        session = get_object_or_404(Session, id=session_id)
        return redirect(reverse('session-list', kwargs={
            'category_slug': session.complex.category.slug,
            'complex_slug': session.complex.slug
        }))


@login_required
def payment(request, reserve_id):
    reserve = get_object_or_404(Reserve, id=reserve_id)
    session = get_object_or_404(Session, id=reserve.session.id)
    complex_instead = get_object_or_404(Complex, id=reserve.session.complex.id)
    context = {
        'reserve': reserve,
        'session': session,
        'complex': complex_instead,
    }
    return render(request, 'payment/payment.html', context)


@login_required()
def send_request(request, reserve_id):
    reserve = get_object_or_404(Reserve, id=reserve_id)
    session = get_object_or_404(Session, id=reserve.session.id)
    amount = session.session_price
    callback_url = f"{CallbackURL}?reserve_id={reserve_id}"
    amount = amount * 1000
    description = f'پرداخت کننده:{reserve.first_name} {reserve.last_name}'
    phone = reserve.user.phone_number
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        "Phone": phone,
        "CallbackURL": callback_url,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_data = response.json()
            if response_data['Status'] == 100:
                return HttpResponseRedirect(ZP_API_STARTPAY + str(response_data['Authority']))

            else:
                return JsonResponse({'status': False, 'code': str(response_data['Status'])})
        return HttpResponse(response.content, status=response.status_code, content_type='application/json')

    except requests.exceptions.Timeout:
        return JsonResponse({'status': False, 'code': 'timeout'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': False, 'code': 'connection error'})


@login_required()
def verify(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    reserve_id = request.GET.get('reserve_id')
    payed_reserve = get_object_or_404(Reserve, id=reserve_id)
    session = get_object_or_404(Session, id=payed_reserve.session.id)

    if status != 'OK':
        return HttpResponse(
            "پرداخت لغو شد ",
            status=400)

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": session.session_price,
        "Authority": authority,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data['Status'] == 100:
            payed_reserve.STATUS = 'تایید شده'
            payed_reserve.save()
            payed = Payment()
            payed.user = payed_reserve.user
            payed.reserve = payed_reserve
            payed.amount = payed_reserve.reserve_total
            payed.user.score += payed.amount
            payed.reserve.session.complex.supervisor.balance += payed.amount
            payed.reserve.session.complex.supervisor.save()
            payed.user.save()
            payed.save()
            messages.error(request, 'پرداخت موفقیت آمیز بود !')
            return redirect(reverse('account:dashboard', kwargs={'phone': payed_reserve.user.phone_number}))
        else:
            payed_reserve.STATUS = 'کنسل شده'
            payed_reserve.save()
            session.is_reserved = False
            session.save()
            messages.error(request, 'پرداخت انجام نشد !')
            return redirect(reverse('account:dashboard', kwargs={'phone': payed_reserve.user.phone_number}))

    else:
        payed_reserve.STATUS = 'کنسل شده'
        payed_reserve.save()
        session.is_reserved = False
        session.save()
        messages.error(request, 'پرداخت انجام نشد !')
        return redirect(reverse('account:dashboard', kwargs={'phone': payed_reserve.user.phone_number}))


@login_required()
def delete(request, reserve_id):
    deleted_reserve = get_object_or_404(Reserve, id=reserve_id)
    session = get_object_or_404(Session, id=deleted_reserve.session.id)
    session.is_reserved = False
    session.save()
    deleted_reserve.delete()
    return redirect('home')
