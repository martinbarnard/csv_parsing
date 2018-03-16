# -*- coding: utf-8 -*-

'''
Bink test
Using Dataset from https://data.gov.uk/dataset/mobile-phone-masts
'''

import csv
import sys
import argparse
import datetime
from operator import itemgetter

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

style = OKGREEN + '{}' + ENDC
stars = lambda n : print(style.format('*'*n))
title = lambda n : print(style.format(n))
class Pole():
    '''
    This is our csv parser. It will parse the CSV.
    Some assumptions are being made about the csv file:
        based on dataset given above...
        Fields are:
            Propery Name | Property Address [1] | Property Address [2] | Property Address [3] | Property Address [4] |
            Unit Name | Tenant Name | Lease Start Date | Lease End Date | Lease Years | Current Rent
        Dates are formatted as "%d %b %Y" format
        We are not normalising names (i.e. Name is not the same as nAme or name)
    '''
    def __init__(self,file):
        self.csv_data = []
        self.mapped_data = {}
        self.read_data(file)

    def read_data(self, file):
        '''
        Read our csv & build our dataset 
        @param file (file handle)
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
            title(e)
            sys.exit(1)

    def rent_ordered(self, num_items = 5, ascending = True, field='Current Rent'):
        '''
        print out the n-items from the list - ordering by field
        '''
        rv = []
        rev = not ascending
        rv = sorted(self.csv_data, key=itemgetter(field), reverse=rev)
        rk = rv[0].keys()
        stars(120)
        title('getting {} items ordered by "{}"'.format(num_items, field))
        stars(120)
        title('\t'.join(p for p in rk))
        for row in rv[:num_items]:
            print('\t'.join(str(row[p]) for p in rk))
            

    def get_lease_info(self, years=25, ascending=True):
        '''
        Will return the items with 25 years lease (['Lease Years'])
        '''
        rev = not ascending
        # filter by our years, sort by our rent
        items = sorted([row for row in self.csv_data if int(row['Lease Years']) == years], key=itemgetter('Current Rent'), reverse=rev)
        # Total our rent
        sum_items = sum([float(p['Current Rent']) for p in items])

        stars(120)
        title('Getting Lease Info')
        stars(120)

        rk = items[0].keys()
        print('\t'.join(p for p in rk))

        for row in items:
            print('\t'.join(str(row[p]) for p in rk))

        title('Total Rent Calculated: {}'.format(sum_items))

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
        title('Leases with Start Dates between {} and {}'.format(date1_string, date2_string))
        stars(120)

        rk = nn[0].keys()
        title('\t'.join(p for p in rk))
        for row in nn:
            print('\t'.join(str(row[p]) for p in row))
        stars(120)


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
        title('Tentant Mast Count')
        stars(120)
        for k,v in sorted(rv.items()):
            print('{}\t\t{}'.format(k,v))


def run():
    '''
    Parse our csv file and display some info
    '''
    years = 25
    rev = False
    rent = True

    # Opts and args
    parser = argparse.ArgumentParser( description = 'csv processor')
    parser.add_argument('-f', '--file', help='csv file to process')
    parser.add_argument('-r', '--rent', action='store_true', default=True, help='csv file to process')
    parser.add_argument('-y', '--years', action='store', help='csv file to process', default=25)
    args = parser.parse_args()

    years = int(args.years)
    rent = args.rent
    f = args.file
    if not f:
        print('No file to open!')
        sys.exit()

    # File opening thang
    try:
        file = open(f)
    except Exception as e:
        print('unable to open {}'.format(arg))
        print(e)
        sys.exit(2)

    if not file:
        print('unable to do stuff without a file')
        sys.exit(0)

    p = Pole(file)

    if rent:
        p.rent_ordered()

    if years:
        title('Getting {} years lease info'.format(years))
        p.get_lease_info(years, rev)

    p.get_tenant_mast_count()
    start_date = datetime.datetime.strptime('01 Jun 1999', '%d %b %Y')
    end_date = datetime.datetime.strptime('31 Aug 2007', '%d %b %Y')

    p.get_lease_between(start_date, end_date)





