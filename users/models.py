from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', '3 Months'),
        ('semiannual', '6 Months'),
        ('yearly', 'Yearly'),
    ]

    PLAN_DURATIONS = {
        'monthly': 30,
        'quarterly': 90,
        'semiannual': 180,
        'yearly': 365,
    }

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.CharField(max_length=12, choices=PLAN_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.active is None:
            self.active = True
        days = self.PLAN_DURATIONS.get(self.plan, 30)
        today = timezone.localdate()
        if not self.end_date or self.end_date < today:
            self.end_date = (today + timedelta(days=days))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan} ({'Active' if self.active else 'Inactive'})"
    @property
    def is_valid(self):
        return self.active and self.end_date >= timezone.localdate()