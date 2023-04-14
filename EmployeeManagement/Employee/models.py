import random
import string
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.utils.html import strip_tags

# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    alternate_number = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=5)
    profile_photo = models.ImageField(upload_to='profile_photos/')
    proof_of_identification = models.FileField(upload_to='proof_of_identification/')
    emergency_contact_name = models.CharField(max_length=50)
    emergency_contact_number = models.CharField(max_length=20)
    emergency_contact_relation = models.CharField(max_length=50)
    permanent_address_street1 = models.CharField(max_length=100)
    permanent_address_city = models.CharField(max_length=50)
    permanent_address_state = models.CharField(max_length=50)
    permanent_address_pincode = models.CharField(max_length=10)
    current_address_street1 = models.CharField(max_length=100)
    current_address_city = models.CharField(max_length=50)
    current_address_state = models.CharField(max_length=50)
    current_address_pincode = models.CharField(max_length=10)
    joining_date = models.DateField()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=20)




    def save(self, *args, **kwargs):
        if not self.pk: # Only on creation
            # Generate dynamic username
            username = f"{self.first_name.lower()}{self.last_name[0].lower()}"
            # Check for duplicate usernames
            i = 1
            while Employee.objects.filter(username=username).exists():
                username = f"{username}{i:02d}"
                i += 1
            self.username = username
            
            # Generate random password
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            print(password)
            self.password = password
            
            # Save the object
            super().save(*args, **kwargs)
            
            # Send welcome email to the employee
            subject = f"Welcome to {settings.COMPANY_NAME}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = self.email
            context = {
                'employee_name': self.first_name,
                'joining_date': self.joining_date.strftime("%B %d, %Y"),
                'joining_day': self.joining_date.strftime("%A"),
                'login_link': "http://example.com/login", # Replace with actual login link
                'username': self.username,
                'password': password,
                'company_name': settings.COMPANY_NAME,
                'system_config_value': settings.SYSTEM_CONFIG_VALUE,
            }
            html_message = render_to_string('welcome_email.html', context)
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Education(models.Model):
    DEGREE_CHOICES = (
        ('Masters', 'Masters'),
        ('Bachelors', 'Bachelors'),
        ('Boards', 'Boards')
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=20)
    institution_name = models.CharField(max_length=100)
    year_of_passing = models.PositiveIntegerField()

    class Meta:
        ordering = ['-year_of_passing']

    def __str__(self):
        return f"{self.degree} ({self.institution_name})"




class Experience(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.company} ({self.start_date} to {self.end_date or 'Present'})"
    




class SystemConfig(models.Model):
    company_logo = models.ImageField(upload_to='system_config/')
    company_name = models.CharField(max_length=100)
    hr_manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)
    smtp_server = models.CharField(max_length=100)
    smtp_port = models.IntegerField()
    smtp_username = models.CharField(max_length=100)
    smtp_password = models.CharField(max_length=100)


class Holiday(models.Model):
    MONTH_CHOICES = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    )

    month = models.IntegerField(choices=MONTH_CHOICES)
    festival_date = models.DateField()
    festival_name = models.CharField(max_length=100)
    day = models.CharField(max_length=10)

    def __str__(self):
                return self.festival_name

    