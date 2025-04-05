import csv
from faker import Faker

fake = Faker()

def generate_fake_sales_data(num_records):
    with open('fake_sales_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'sales']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for _ in range(num_records):
            writer.writerow({
                'date': fake.date_this_decade(),  # Generate random date
                'sales': fake.random_int(min=100, max=1000)  # Generate random sales
            })

    print('Fake sales data generated!')

generate_fake_sales_data(30)  # Generate 30 records
