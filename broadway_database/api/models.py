from django.db import models

# Create your models here.
class Show(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    show_type = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.name


class Production(models.Model):
    theatre_name = models.CharField(max_length=100 , primary_key=True)
    show = models.ForeignKey(Show , on_delete=models.CASCADE, related_name='productions')
    total_seats = models.IntegerField(null=True)
    open_data = models.DateField(null=True)
    close_date = models.DateField(null=True)
    preview_data = models.DateField(null=True)
    intermissions = models.IntegerField(null=True)
    production_type = models.CharField(max_length=50, null=True)
    run_time = models.IntegerField(null=True)
    address = models.CharField(max_length=500, null=True)
    performances = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.show}: {self.theatre_name}'


class Grosses(models.Model):
    # id = models.CharField(max_length=250)
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='grosses')
    week = models.DateField(null=True)
    week_num = models.IntegerField(null=True)
    gross = models.FloatField(null=True)
    potential_gross = models.FloatField(null=True)
    avg_ticket_price = models.FloatField(null=True)
    top_ticket_price = models.FloatField(null=True)
    seats_sold = models.IntegerField(null=True)
    capacity_of_available_seats = models.FloatField(null=True)

    def __str__(self):
        return f'Production: {self.production}, Week: {self.week}, Gross: {self.gross}'
