# انتخاب ایمیج پایه
FROM python:3.10-slim

# تنظیم دایرکتوری کاری در کانتینر
WORKDIR /app

# کپی کردن فایل‌های مورد نیاز به کانتینر
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


# کپی دیتابیس
COPY db.sqlite3 /app/db.sqlite3

COPY . .


# اجرای دستورات مدیریت پروژه جنگو
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# باز کردن پورت 8000 برای دسترسی به اپلیکیشن
EXPOSE 8000

# دستور برای اجرای سرور جنگو
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]