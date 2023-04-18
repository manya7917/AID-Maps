import csv
import random

def generate_service_number():
    return random.randint(10000, 99999)

headers = ['City', 'Name of Personnel', 'Service Number', 'Headquarters Address']


namelist = ['Manya','Tanmay','Sharma','Verma','Rana','Raju','Kotak Mahindra']
HQs =['KAILASH HOSPITAL', 'APOLLO', 'FORTIS']

data = []

with open('manya.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    rows = [row for row in reader]
    
random_row = random.choice(rows)
print(random_row)