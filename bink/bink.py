# -*- coding: utf-8 -*-

'''
Bink test
Using Dataset from https://data.gov.uk/dataset/mobile-phone-masts
'''

import csv
from os import path
import sys
from operator import itemgetter
import datetime

# Our deps
import click

stars = lambda n : click.echo('*'*n)
class Pole():
    '''
    Our mast data
    '''
    def __init__(self,file):
        '''
        '''
        self.csv_data = []
        self.mapped_data = {}
        self.read_data(file)

    def read_data(self, file):
        '''
        Read data & populate it in list. Do other stuff with it later
        We know that Lease Start Date and Lease End Date are dates
        We know that Lease Years are int & Current Rent are floats
        '''
        try:
            reader = csv.DictReader(file)
            for row in reader:
                self.csv_data.append(row)
                # Create a dict of lists
                for k,v in row.items():
                    if k in self.mapped_data:
                        self.mapped_data[k].append(v)
                    else:
                        self.mapped_data[k] = [v]
            return True
        except Exception as e:
            click.echo(e)
            sys.exit(1)

    def rent_ordered(self, num_items = 5, ascending = True):
        '''
        Return the n-items from the list 
        '''
        rv = []
        rev = not ascending
        rv = sorted(self.csv_data, key=itemgetter('Current Rent'), reverse=rev)
        rk = rv[0].keys()
        stars(120)
        click.echo('getting the rent ({} items)'.format(num_items))
        stars(120)
        click.echo('\t'.join(p for p in rk))
        for row in rv[:num_items]:
            nr = row
            click.echo('\t'.join(str(row[p]) for p in rk))
            

    def get_lease_info(self, years=25, ascending=True):
        '''
        Will return the items with 25 years lease (['Lease Years'])
        '''
        rev = not ascending
        items = sorted([row for row in self.csv_data if int(row['Lease Years']) == years], key=itemgetter('Current Rent'), reverse=rev)
        sum_items = sum([float(p['Current Rent']) for p in items])
        stars(120)
        click.echo(' ----- Total Rent calculated: {}'.format(sum_items))
        stars(120)
        click.echo('getting lease info')
        stars(120)
        rk = items[0].keys()
        st = '\t'.join(p for p in rk)
        click.echo('\t'.join(p for p in rk))

        for row in items:
            click.echo('\t'.join(str(row[p]) for p in rk))

    def get_lease_between(self, date1, date2):
        '''
        Will return the leases with start dates between date1 & date2
        '''
        date1_string = datetime.datetime.strftime(date1, '%d/%m/%Y')
        date2_string = datetime.datetime.strftime(date2, '%d/%m/%Y')
        # first map the Lease Start Date 
        nn = []
        for row in self.csv_data:
            sd_date = datetime.datetime.strptime(row['Lease Start Date'], '%d %b %Y')
            sd_string = datetime.datetime.strftime(sd_date, '%d/%m/%Y')
            ed_string = datetime.datetime.strftime(
                datetime.datetime.strptime(row['Lease End Date'], '%d %b %Y'),
                '%d/%m/%Y'
            )

            if sd_date >= date1 and sd_date <= date2:
                row['Lease Start Date'] = sd_string
                row['Lease End Date'] = ed_string
                nn.append(row)

        stars(120)
        click.echo('Leases with Start Dates between {} and {}'.format(date1_string, date2_string))
        stars(120)

        for row in nn:
            click.echo('\t'.join(str(row[p]) for p in row))


    def get_tenant_mast_count(self):
        '''
        Will print out the count of masts for each tenant. Normalising names?
        '''
        rv = {}
        for row in self.csv_data:
            if row['Tenant Name'] in rv:
                rv[row['Tenant Name']] +=1
            else:
                rv[row['Tenant Name']] = 1
        stars(120)
        click.echo('Tentant Mast Count')
        stars(120)
        for k,v in sorted(rv.items()):
            click.echo('{}\t\t{}'.format(k,v))


@click.command()
@click.option('--years', type=click.INT, help='Print the # years lease')
@click.option('--rent', type=click.INT, help='Print the rent')
@click.option('--reverse', type=click.BOOL, help='Used to reverse normal output order')
@click.option('--num', type=click.INT, help='Number of items to print')
@click.argument('file', type=click.File('r'))
def run(file, years, rent, reverse, num):
    '''
    Parse our csv file and display some info
    '''
    rev = False
    p = Pole(file)
    if reverse:
        rev = True

    if rent:
        p.rent_ordered()

    if years:
        click.echo('Getting {} years lease info'.format(years))
        p.get_lease_info(years, rev)

    p.get_tenant_mast_count()
    start_date = datetime.datetime.strptime('01 Jun 1999', '%d %b %Y')
    end_date = datetime.datetime.strptime('31 Aug 2007', '%d %b %Y')

    p.get_lease_between(start_date, end_date)





