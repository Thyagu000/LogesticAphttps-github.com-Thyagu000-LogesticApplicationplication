from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# ✅ NEW MODEL
class Quote(models.Model):
    service = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return self.name