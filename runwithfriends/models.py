from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Run(models.Model):

    user = models.ForeignKey(User, related_name="runs")
    location = models.CharField(max_length=100,)
    distance = models.FloatField(max_length=100,)
    date = models.DateField()

    @property
    def pretty_distance(self):
        return u'%.2f' % self.distance


