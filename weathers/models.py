from django.db import models


# Create your models here.
class WeatherDB(models.Model):
    stn = models.FloatField(blank=True, null=True)
    temp_max = models.FloatField(blank=True, null=True)
    temp_min = models.FloatField(blank=True, null=True)
    rain = models.FloatField(blank=True, null=True)
    wind_max = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.temp)