import os
import csv
from datetime import datetime
from collections import namedtuple
#points us to our project settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE','broadway_database.settings')
import django
#sets up the django evnironment so that we can import models
django.setup()
from api.models import Show, Production, Grosses

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# path to each csv file
GROSSES = os.path.join(BASE_DIR,'Test_Data', 'broadway_grosses_truncated_just_because.csv')
SILVER = os.path.join(BASE_DIR, 'Test_Data', 'broadway_silver.csv')

# data structure for each row of the SILVER csv
Silver = namedtuple('Silver',['index', 'open_date', 'close_date',
    'preview_date', 'intermissions', 'market', 'production_type', 'run_time', 'run_time_str',
    'run_type', 'name', 'show_type', 'theatre_name', 'address'] )

# data structure for each row of the GROSSES csv
Gross = namedtuple('Grosses', ['index', 'week', 'week_num', 'gross',
    'gross_diff', 'pot_gross', 'potential_gross_percent', 'average_paid_ticket',
    'top_ticket', 'seats_sold', 'total_seats', 'performances', 'capacity',
    'capacity_diff', 'show_name'])

def datetime_or_none(value):
    '''handles empty date values in our csv'''
    if value:
        return datetime.strptime(value, '%m/%d/%y').date()
    return

def int_or_none(value):
    '''handles empty int values in our csv'''
    if value:
        return int(value)
    return

def str_or_none(value):
    '''handles empty str values in our csv'''
    if value:
        return value
    return

def process_dollar_str(value):
    '''convert strings with "$" and "," to floats'''
    return float(value.replace('$', '').replace(',', ''))

def process_percent_str(value):
    '''convert strings with "%" to floats'''
    return float(value.replace('%', ''))

if __name__ == '__main__':
    #process silver data
    with open(SILVER) as csvfile:
        reader = csv.reader(csvfile)
        # skip the header row
        next(reader)
        # loop through each remaining row
        for row in reader:
            show_data = Silver(*row)
            # create the show if it doesn't exist
            show, _ = Show.objects.get_or_create(
                name=show_data.name.strip(),
                show_type=show_data.show_type
            )
            print( f'ADDING {show} TO THE DATABASE')
            # create the production if it doesn't exist
            prod, _ = Production.objects.get_or_create(
                theatre_name=show_data.theatre_name,
                show=show,
            )
            # add extra fields to the production
            prod.open_data = datetime_or_none(show_data.open_date)
            prod.close_date = datetime_or_none(show_data.close_date)
            prod.preview_data = datetime_or_none(show_data.preview_date)
            prod.intermissions = int_or_none(show_data.intermissions)
            prod.production_type = str_or_none(show_data.production_type)
            prod.run_time = int_or_none(show_data.run_time)
            prod.address = str_or_none(show_data.address)
            prod.save()
            print( f'\tADDING NEW PRODUCTION - {prod} - TO THE DATABASE')

    # process grosses data:
    with open(GROSSES) as csvfile:
        reader = csv.reader(csvfile)
        # skip the header row
        next(reader)
        #keep track of the current production within the loop
        current_prod = None
        # loop through the remaining rows
        for row in reader:
            g = Gross(*row) # not the best variable name
            prod = Production.objects.get(show=g.show_name)

            #check to make sure we only save the prod info once
            if prod != current_prod:
                current_prod = prod
                current_prod.total_seats = int_or_none(g.total_seats)
                current_prod.performances = int_or_none(g.performances)
                current_prod.save()
                print(f'ADDING FIELDS: total_seats, and performances to {current_prod}')

            gross, _ = Grosses.objects.get_or_create(
                production = current_prod,
                week = datetime_or_none(g.week),
                week_num = int_or_none(g.week_num),
            )
            gross.gross = process_dollar_str(g.gross)
            gross.potential_gross = process_dollar_str(g.gross)
            gross.avg_ticket_price = process_dollar_str(g.average_paid_ticket)
            gross.top_ticket_price = process_dollar_str(g.top_ticket)
            gross.seats_sold = int_or_none(g.seats_sold)
            gross.capacity_of_available_seats = process_percent_str(g.capacity)
            gross.save()
            print(f'\t ADDING GROSSES DATA FOR {gross}')
