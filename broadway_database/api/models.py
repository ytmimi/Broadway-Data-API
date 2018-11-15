from django.db import models

# Create your models here.
class Show(models.Model):
    name = models.CharField(max_lenght=200, primary_key=True)
    show_type = models.CharField(max_length=25, null=True)


class Production(models.Model):
    theatre_name = models.CharField(max_lenght=100 , primary_key=True)
    show = models.ForeignKey(Show , on_delete=models.CASCADE, related_name='productions')
    total_seats = models.IntegerField(null=True)
    open_data = models.DateField(null=True)
    close_date = models.DateField(null=True)
    preview_data = models.DateField(null=True)
    intermissions = models.IntegerField(null=True)
    production_type = models.CharField(max_lenght=50, null=True)
    run_time = models.IntegerField(null=True)


class Grosses(models.Model):
    id = models.CharField(max_lenght=250)
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='grosses')
    week = models.DateField()
    week_num = models.IntegerField()
    gross = models.FloatField()
    potential_gross = models.FloatField()
    seats_sold = models.IntegerField()
    capacity_of_available_seats = models.IntegerField()
