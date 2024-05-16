from django.db import models

class Crawling(models.Model):

    search = models.CharField(max_length=10)
    start_p = models.IntegerField()
    end_p = models.IntegerField()

class CrawlingSubject(models.Model):

    num = models.IntegerField(null=True)
    subject = models.CharField(max_length=10)
    ref = models.CharField(max_length=100)

# Create your models here.
