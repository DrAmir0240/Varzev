from django.test import TestCase
import datetime
import jdatetime

# Create your tests here.
str_input_time = '1401-02-03'
print(str_input_time)
jalali_input_time = jdatetime.datetime.strptime(str_input_time, '%Y-%m-%d')
print(jalali_input_time)
input_time = jalali_input_time.togregorian()
print(input_time)
gregorian_datetime = datetime.date(input_time.year, input_time.month, input_time.day)
print(gregorian_datetime)
