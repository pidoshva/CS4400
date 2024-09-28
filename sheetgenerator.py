"""Fake Excel sheet generetor according to the structure provided by the Utah County"""
import pandas as pd
from faker import Faker
from random import choice
from datetime import timedelta, date

# Initialize Faker instance
fake = Faker()

# List of some example counties
county_list = [
    "Salt Lake County", "Utah County", "Davis County", "Weber County",
    "Washington County", "Cache County", "Summit County", "Tooele County",
    "Box Elder County", "Iron County"
]

# Function to generate birthdates of children under 4 years
def generate_child_dob():
    today = date.today()
    # Generate a birthdate between today and 3 years and 9 months ago
    max_age = timedelta(days=365 * 3 + 9 * 30)  # 3 years and 9 months
    birth_date = today - timedelta(days=fake.random_int(min=0, max=max_age.days))
    return birth_date

# Function to generate the "Database" data
def generate_database_data(num_entries=200):
    database_data = []
    for _ in range(num_entries):
        child_last_name = fake.last_name()
        child_first_name = fake.first_name()
        child_middle_name = fake.first_name()
        dob = generate_child_dob().strftime("%Y-%m-%d")
        mom_last_name = fake.last_name()
        mom_first_name = fake.first_name()
        state_file_number = fake.unique.random_number(digits=9)
        database_data.append([
            child_last_name, child_first_name, child_middle_name, dob, 
            mom_last_name, mom_first_name, state_file_number
        ])
    return pd.DataFrame(database_data, columns=[
        "Child Last Name", "Child First Name", "Child Middle Name", "DOB", 
        "Mother Last Name", "Mother First Name", "State File Number"
    ])

# Function to generate the "Email List" (Medicaid List) data
def generate_medicaid_data(num_entries=200):
    medicaid_data = []
    for _ in range(num_entries):
        mom_first_name = fake.first_name()
        last_name = fake.last_name()  # Mother's last name
        mom_dob = fake.date_of_birth(minimum_age=18, maximum_age=50).strftime("%Y-%m-%d")
        child_dob = generate_child_dob().strftime("%Y-%m-%d")
        child_id = fake.unique.random_number(digits=5)
        case_id = fake.unique.random_number(digits=9)
        phone_number = fake.phone_number()
        mobile_number = fake.phone_number()
        street = fake.street_address()
        city = fake.city()
        state = fake.state_abbr()
        zip_code = fake.zipcode()
        county = choice(county_list)  # Randomly select a county from the list
        tobacco_usage = fake.boolean(chance_of_getting_true=10)  # 10% chance
        utah_first_time_man = fake.boolean(chance_of_getting_true=20)  # 20% chance
        medicaid_data.append([
            mom_first_name, last_name, mom_dob, child_id, child_dob, 
            case_id, phone_number, mobile_number, street, city, state, zip_code, 
            county, tobacco_usage, utah_first_time_man
        ])
    return pd.DataFrame(medicaid_data, columns=[
        "Mother First Name", "Last Name", "Mother DOB", "Child ID", "Child DOB", 
        "Case ID", "Phone #", "Mobile #", "Street", "City", "State", "ZIP", 
        "County", "Tobacco Usage", "Utah First Time Man."
    ])

# Function to verify that all names are present in both sheets
def verify_names(database_file, medicaid_data_file):
    # Load the two Excel files
    database_df = pd.read_excel(database_file)
    medicaid_df = pd.read_excel(medicaid_data_file)
    
    # Extract child and mother names from both DataFrames
    database_names = set(database_df["Mother First Name"] + " " + database_df["Mother Last Name"])
    medicaid_names = set(medicaid_df["Mother First Name"] + " " + medicaid_df["Last Name"])
    
    # Check for missing or extra names
    missing_in_medicaid = database_names - medicaid_names
    missing_in_database = medicaid_names - database_names
    
    if not missing_in_medicaid and not missing_in_database:
        print("All names match in both sheets! No missing or extra names.")
    else:
        if missing_in_medicaid:
            print("Names in Database but missing in Medicaid list:", missing_in_medicaid)
        if missing_in_database:
            print("Names in Medicaid list but missing in Database:", missing_in_database)

# Main function to generate the files
def generate_excel_files():
    # Generate data
    database_data_df = generate_database_data(200)
    medicaid_data_df = generate_medicaid_data(200)

    # Save the data to Excel files
    database_filename = "database_data_200.xlsx"
    medicaid_data_filename = "medicaid_data_200.xlsx"
    
    database_data_df.to_excel(database_filename, index=False)
    medicaid_data_df.to_excel(medicaid_data_filename, index=False)
    
    print(f"Files created: {database_filename}, {medicaid_data_filename}")
    
    # Verify that all names are present in both files
    verify_names(database_filename, medicaid_data_filename)

# Run the program
if __name__ == "__main__":
    generate_excel_files()
