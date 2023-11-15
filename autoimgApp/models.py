from django.db import models

# Create your models here.


class WorkingDB(models.Model):
    slID = models.AutoField(primary_key=True)
    selectFile = models.FileField(null=True, blank=True, upload_to="FileDBFolder")
    # def __str__(self):
    #     return self.selectFile.url

class ContactMessage(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=12)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    dateee = models.DateField()
    def __str__(self):
        return self.fullname