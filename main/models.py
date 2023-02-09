from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    sections = models.IntegerField(default=5, null=False)