from django.contrib import admin
from .models import User, Service, Application, Payment, Notification, Document

admin.site.register(User)
admin.site.register(Service)
admin.site.register(Application)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(Document)
