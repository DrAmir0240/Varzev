from datetime import timedelta, datetime
import jdatetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from account.models import User
from .models import Complex, Session, Category


# Create your views here.
def home(request):
    complexes = Complex.objects.all().filter(is_active=True).order_by('id')
    context = {
        'complexes': complexes,
    }
    return render(request, 'home.html', context)


def complexes_list(request, category_slug=None):
    categories = None
    complexes = None
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        complexes = Complex.objects.filter(category=categories, is_active=True)
        paginator = Paginator(complexes, 1)
        page = request.GET.get('page')
        paged_complexes = paginator.get_page(page)
        complexes_count = complexes.count()
    else:
        complexes = Complex.objects.all().filter(is_active=True).order_by('id')
        paginator = Paginator(complexes, 9)
        page = request.GET.get('page')
        paged_complexes = paginator.get_page(page)
        complexes_count = complexes.count()
    context = {
        'complexes': paged_complexes,
        'complexes_count': complexes_count,
    }
    return render(request, 'complex/complex-list.html', context)


def complexes_detail(request, category_slug, complex_slug):
    try:
        single_complex = Complex.objects.get(category__slug=category_slug, slug=complex_slug)
    except Exception as e:
        raise e

    context = {
        'single_complex': single_complex,
    }

    return render(request, 'complex/complex-detail.html', context)


@login_required
def create_complex(request):
    categories = Category.objects.all()
    complecs = Complex()
    user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        print(request.POST)
        complecs.supervisor = user
        complecs.complex_name = request.POST['complex_name']
        complecs.complex_description = request.POST['complex_description']
        complecs.complex_img = request.POST['complex_img']
        category_post = request.POST['category']
        print(category_post)
        category = get_object_or_404(Category, category_name=category_post)
        complecs.category = category
        complecs.area = request.POST['area']
        variation = request.POST.get('price_variation')
        price_variation = bool(variation)
        print(price_variation)
        complecs.price_variation = price_variation
        complecs.price = request.POST['price']
        complecs.Address = request.POST['Address']
        complecs.city = request.POST['city']
        complecs.neighborhood = request.POST['zone']
        complecs.guards_count = request.POST['guards_count']
        complecs.start_time = request.POST['start_time']
        complecs.end_time = request.POST['end_time']
        complecs.session_long = int(request.POST['session_long'])
        complecs.close_days = request.POST['close_days']
        complecs.is_active = False
        complecs.save()
        messages.success(request, "مجموعه شما با موفقیت ثبت شد منتظر تایید بمانید...")
        return redirect(reverse('account:supervisor-dashboard', kwargs={'phone': user.phone_number}))

    else:
        return render(request, 'complex/create-complex.html', {'categories': categories})


def session_list(request, category_slug, complex_slug):
    date = jdatetime.date.today()
    print(date)
    if request.method == 'POST':
        posted_date = request.POST['date']
        print(posted_date)
        date = datetime.strptime(posted_date, '%Y/%m/%d').strftime('%Y-%m-%d')
        print(date)

    complex_instance = get_object_or_404(Complex, slug=complex_slug)
    sessions = Session.objects.filter(complex=complex_instance, date=date).order_by('time')
    user_is_supervisor = (complex_instance.supervisor == request.user)

    context = {
        'complex': complex_instance,
        'sessions': sessions,
        'user_is_supervisor': user_is_supervisor,
        'date': date
    }

    return render(request, 'complex/session-list.html', context)


def create_sessions(request, category_slug, complex_slug):
    session_complex = get_object_or_404(Complex, slug=complex_slug)
    today_1 = datetime.today()
    today = datetime.date(today_1)
    print(today)
    if request.method == 'POST':
        print(request.POST)
        str_start_date = request.POST.get('start_date')
        str_end_date = request.POST.get('end_date')
        print(f'received {str_start_date} and {str_end_date} correctly')
        try:
            start_date_jalali = jdatetime.datetime.strptime(str_start_date, '%Y-%m-%d')
            end_date_jalali = jdatetime.datetime.strptime(str_end_date, '%Y-%m-%d')
            start_date_gregorian = start_date_jalali.togregorian()
            end_date_gregorian = end_date_jalali.togregorian()
            start_date = datetime.date(start_date_gregorian)
            end_date = datetime.date(end_date_gregorian)
            print(f'received {start_date} and {end_date}')
        except ValueError as e:
            messages.error(request, 'فرمت تاریخ ورودی نادرست است.')
            return redirect(
                reverse('create-session', kwargs={'category_slug': category_slug, 'complex_slug': complex_slug}))
        if start_date < today:
            messages.error(request, 'از تاریخ شروع ورودی گذشته است لطفا تاریخ ورودی را درست وارد کنید')
            return redirect(
                reverse('create-session', kwargs={'category_slug': category_slug, 'complex_slug': complex_slug}))
        else:
            if end_date <= start_date:
                messages.error(request,
                               'تاریخ پایان ورودی از تاریخ شروع ورودی عقب تر است لطفا تاریخ ورودی را درست وارد کنید')
                return redirect(
                    reverse('create-session', kwargs={'category_slug': category_slug, 'complex_slug': complex_slug}))
            else:
                day_count = (end_date - start_date).days + 1
                for single_date in [start_date + timedelta(n) for n in range(day_count)]:
                    if single_date > end_date:
                        break
                    start = datetime.combine(single_date, session_complex.start_time)
                    end = datetime.combine(single_date, session_complex.end_time)
                    step = timedelta(minutes=int(session_complex.session_long))
                    current_time = start

                    while current_time <= end - step:
                        session_time = current_time.strftime('%H:%M')
                        Session.objects.create(
                            date=single_date,
                            time=session_time,
                            complex=session_complex,
                            session_price=session_complex.price
                        )
                        current_time += step

                return redirect(
                    reverse('session-list', kwargs={'category_slug': category_slug, 'complex_slug': complex_slug}))

    else:
        return render(request, 'complex/create-session.html', {'complex': session_complex})


@login_required
def edit_session(request, category_slug, complex_slug, session_id):
    if request.method == 'POST':
        session = get_object_or_404(Session, id=session_id)
        is_available = request.POST.get('is_available')
        print(is_available)
        session_price = str(request.POST.get('session_price'))
        print(session_price)
        print(bool(is_available))
        session.is_available = bool(is_available)
        session.session_price = session_price
        session.save()
        return redirect(reverse('session-list',
                                kwargs={"category_slug": category_slug,
                                        'complex_slug': complex_slug, }))
    else:
        session = get_object_or_404(Session, id=session_id)
        return render(request, 'complex/edit-session.html', {'session': session})


def search(request):
    complexes = 0
    context = 0
    complex_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            complexes = Complex.objects.filter(
                Q(complex_description__icontains=keyword) | Q(
                    complex_name__icontains=keyword))
            product_count = complexes.count()

        context = {
            'complexes': complexes,
            'complex_count': complex_count,
        }
    return render(request, 'complex/complex-list.html', context)
