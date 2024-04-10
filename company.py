import csv
from masters.models import Company

def import_company_data(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create Company instance
            company_instance = Company.objects.create(
                company_name=row['company_name'],
                company_contact_no=row['company_contact_no'],
                address=row['address'],
                company_suffix=row['company_suffix'] if 'company_suffix' in row else None,
                is_customer=row['is_customer'].lower() == 'true',
                is_self_company=row['is_self_company'].lower() == 'true',
            )

if __name__ == '__main__':
    csv_file_path = 'D:\Helpdesk\result.csv'
    import_company_data(csv_file_path)
