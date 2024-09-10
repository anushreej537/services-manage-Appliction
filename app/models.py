from django.contrib.auth.models import AbstractUser
from django.db import models

# class User(AbstractUser):
#     ROLE_CHOICES = [
#         ('employee', 'Employee'),
#         ('admin', 'Admin'),
#         ('super_admin', 'Super Admin'),
#     ]
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
#     otp = models.CharField(max_length=6, blank=True, null=True)  # For OTP verification

#     def __str__(self):
#         return self.username
    

class User(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    otp = models.CharField(max_length=6, blank=True, null=True)  # For OTP verification

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Added related_name to avoid conflicts
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Added related_name to avoid conflicts
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    timeline = models.CharField(max_length=100)  # e.g., "3 days", "1 week"
    document_requirements = models.TextField()  # Can store required documents as text

    def __str__(self):
        return self.name
    

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    documents = models.ManyToManyField('Document', blank=True, related_name='applications')  # Related name added here
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, default='unpaid')  # Paid, Unpaid

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('advance', 'Advance'),
        ('balance', 'Balance'),
        ('completed', 'Completed'),
    ]
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Example: 9999.99
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)

    def __str__(self):
        return f"Payment for {self.application.id} - {self.status}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


class Document(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='application_documents')  # Related name added here
    document_type = models.CharField(max_length=255)  # Example: Passport, Registration Certificate
    document_file = models.FileField(upload_to='documents/')
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.document_type} for Application {self.application.id}"

