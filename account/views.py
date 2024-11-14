from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator

from complex.models import Complex, Session
from payment.models import Reserve, Payment
from .models import User, Settlements
from rest_framework.views import APIView
from .forms import RegistrationForm, SupervisorRegistrationForm

from django.contrib import messages
from django.views import View


class RegisterUser(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', context={'form': form})

    def post(self, request):

        phone_number = request.POST['phone_number']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "حساب کاربری بااین شماره تلفن وجود دارد.")
            return redirect('account:login')

        request.session['phone_number'] = phone_number
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['password'] = password
        request.session['role'] = 3

        # Create user instance (not saved in database yet)
        user = User(phone_number=phone_number, first_name=first_name, last_name=last_name)

        otp = user.send_otp()
        if otp:
            request.session['otp'] = otp
            messages.success(request, "کد اعتبار سنجی برای شما ارسال شد !")
            return redirect('account:verify_otp')
        else:
            messages.error(request, "کد اعتبار سنجی ارسال نشد لطفا بعدا امتحان کنید !")
            return redirect('account:register')


class SuperVisorRegister(View):
    def get(self, request):
        form = SupervisorRegistrationForm()
        return render(request, 'account/supervisor-register.html', context={'form': form})

    def post(self, request):
        phone_number = request.POST['phone_number']
        national_code = request.POST['national_code']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        birth_date = request.POST['birth_date']
        city = request.POST['city']
        zone = request.POST['zone']
        delivery_date = request.POST['delivery_date']
        sheba_name = request.POST['sheba_name']
        sheba_number = request.POST['sheba_number']
        income_settlement = request.POST['income_settlement']

        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "حساب کاربری بااین شماره تلفن وجود دارد.")
            return redirect('account:login')

        request.session['phone_number'] = phone_number
        request.session['national_code'] = national_code
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['password'] = password
        request.session['email'] = email
        request.session['birth_date'] = birth_date
        request.session['city'] = city
        request.session['zone'] = zone
        request.session['delivery_date'] = delivery_date
        request.session['sheba_name'] = sheba_name
        request.session['sheba_number'] = sheba_number
        request.session['income_settlement'] = income_settlement
        request.session['role'] = 4
        user = User(phone_number=phone_number, first_name=first_name)
        otp = user.send_otp()
        if otp:
            request.session['otp'] = otp
            print(otp)
            messages.success(request, "کد اعتبار سنجی برای شما ارسال شد !")
            return redirect('account:verify_otp')
        else:
            messages.error(request, "کد اعتبار سنجی ارسال نشد لطفا بعدا امتحان کنید !")
            return redirect('account:register-supervisor')


class VerifyOTPView(View):
    def get(self, request):
        return render(request, 'account/verify-otp.html')

    def post(self, request):
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        print(saved_otp)

        if entered_otp == saved_otp:
            phone_number = request.session.get('phone_number')
            national_code = request.session.get('national_code')
            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')
            password = request.session.get('password')
            email = request.session.get('email')
            birth_date = request.session.get('birth_date')
            city = request.session.get('city')
            zone = request.session.get('zone')
            delivery_date = request.session.get('delivery_date')
            sheba_name = request.session.get('sheba_name')
            sheba_number = request.session.get('sheba_number')
            role = request.session.get('role')
            income_settlement = request.session.get('income_settlement')
            user = User.objects.create_user(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            user.national_code = national_code
            user.email = email
            user.birth_date = birth_date
            user.city = city
            user.zone = zone
            user.delivery_date = delivery_date
            user.sheba_name = sheba_name
            user.sheba_number = sheba_number
            user.income_settlement = income_settlement
            user.role = role
            user.score = 0
            user.balance = 0
            user.is_active = True
            user.save()
            # Log the user in
            login(request, user)
            messages.success(request, "حساب شما با موفقیت ساخته شد و وارد آن شدید")
            return redirect(reverse('account:dashboard',
                                    kwargs={'phone': user.phone_number}))

        else:
            messages.error(request, "کد اعتبار سنجی صحیح نیست لطفا مجددا امتحان کنید")
            return redirect('account:verify_otp')


class Login(View):
    """
    View class for user login.

    Methods:
    - get: Handles GET requests for login page.
    - post: Handles POST requests for user login form submission.
    """

    def get(self, request):
        """
        Handles GET requests for login page.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Rendered login page.
        """
        return render(request, 'account/login.html')

    def post(self, request):
        """
        Handles POST requests for user login form submission.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Redirects to dashboard page if login is successful, otherwise redirects back to login page
          with error message.
        """
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        # احراز هویت کاربر با استفاده از شماره تلفن و رمز عبور
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            # ورود کاربر به سیستم
            login(request, user)
            messages.success(request, "با موفقیت وارد حساب کاربری خود شدید")

            # هدایت کاربر به داشبورد مناسب براساس نقش کاربری
            if user.role == 3:
                return redirect(reverse('account:dashboard', kwargs={'phone': phone_number}))
            elif user.role == 4:
                return redirect(reverse('account:supervisor-dashboard', kwargs={'phone': phone_number}))
            else:
                return redirect('home')
        else:
            # نمایش پیام خطا در صورت عدم تطابق شماره تلفن یا رمز عبور
            messages.error(request, "شماره تلفن یا رمز ورود نادرست است")
            return redirect('account:login')


@method_decorator(login_required(login_url='account:login'), name='dispatch')
class Logout(APIView):
    """
    View class for user logout.

    Methods:
    - get: Handles GET requests for user logout.
    """

    def get(self, request):
        """
        Handles GET requests for user logout.

        Args:
        - request: HTTP request object.

        Returns:
        - HttpResponse: Redirects to login page after successful logout with success message.
        """
        logout(request)
        messages.success(request, "!با موفقیت از حساب کاربری خارج شدید")
        return redirect('account:login')


@login_required()
def supervisor_dashboard(request, phone):
    user = get_object_or_404(User, phone_number=phone)
    complexes = Complex.objects.filter(supervisor=request.user)
    balance = user.balance
    # اصلاح کوئری:
    reserves = Reserve.objects.filter(session__complex__in=list(complexes))
    payments = Payment.objects.filter(reserve__session__complex__in=list(complexes))
    payments_count = len(list(payments))
    # balance = 0
    # for payment in payments:
    #     balance += payment.amount

    context = {
        'complexes': complexes,
        'user': user,
        'phone': phone,
        'reserves': reserves,
        'payments': payments,
        'payments_count': payments_count,
        'balance': balance
    }

    return render(request, 'account/supervisor-dashboard.html', context=context)


@login_required()
def dashboard(request, phone):
    user = get_object_or_404(User, phone_number=phone)
    reserves = Reserve.objects.filter(user=user, is_reserved=False)
    payments = Payment.objects.filter(user=user)
    payments_count = len(list(payments))
    context = {
        'user': user,
        'reserves': reserves,
        'payments': payments,
        'payments_count': payments_count,
    }
    return render(request, 'account/dashboard.html', context=context)
