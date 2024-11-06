import pandas as pd
from faker import Faker
from datetime import timedelta, date
import random

# Initialize Faker instance
fake = Faker()

# Function to generate birthdates of children under 4 years
def generate_child_dob():
    today = date.today()
    max_age = timedelta(days=365 * 3 + 9 * 30)  # 3 years and 9 months
    birth_date = today - timedelta(days=fake.random_int(min=0, max=max_age.days))
    return birth_date

# Function to generate names, birthdates, and use them for both Database and Medicaid list
def generate_shared_data(num_entries=1000):
    shared_data = []
    for _ in range(num_entries):
        child_last_name = fake.last_name()
        child_first_name = fake.first_name()
        child_middle_name = fake.first_name()
        mom_last_name = fake.last_name()
        mom_first_name = fake.first_name()
        child_dob = generate_child_dob().strftime("%Y-%m-%d")
        mother_id = fake.unique.random_number(digits=9)  # Generate unique mother ID
        shared_data.append({
            "child_last_name": child_last_name,
            "child_first_name": child_first_name,
            "child_middle_name": child_middle_name,
            "mom_last_name": mom_last_name,
            "mom_first_name": mom_first_name,
            "child_dob": child_dob,
            "mother_id": mother_id
        })
    return shared_data

# Function to generate the "Database" data
def generate_database_data(shared_data):
    database_data = []
    for entry in shared_data:
        state_file_number = fake.unique.random_number(digits=9)
        database_data.append([
            entry["child_last_name"], entry["child_first_name"], entry["child_middle_name"], entry["child_dob"], 
            entry["mom_last_name"], entry["mom_first_name"], state_file_number
        ])
    return pd.DataFrame(database_data, columns=[
        "Child Last Name", "Child First Name", "Child Middle Name", "DOB", 
        "Mother Last Name", "Mother First Name", "State File Number"
    ])

# Function to generate the "Medicaid List" data with added Mother ID
def generate_medicaid_data(shared_data, unmatched_entries=0, unmatched_target="both"):
    database_data = []
    medicaid_data = []
    for entry in shared_data:
        mom_dob = fake.date_of_birth(minimum_age=18, maximum_age=50).strftime("%Y-%m-%d")
        child_id = fake.unique.random_number(digits=5)
        case_id = fake.unique.random_number(digits=9)
        phone_number = fake.phone_number()
        mobile_number = fake.phone_number()
        street = fake.street_address()
        city = fake.city()
        state = "UT"
        zip_code = fake.zipcode()
        county = "Utah County"
        tobacco_usage = fake.boolean(chance_of_getting_true=10)
        utah_first_time_man = fake.boolean(chance_of_getting_true=20)
        medicaid_data.append([
            entry["mom_first_name"], entry["mom_last_name"], mom_dob, entry["mother_id"], child_id, entry["child_dob"], 
            case_id, phone_number, mobile_number, street, city, state, zip_code, 
            county, tobacco_usage, utah_first_time_man
        ])

        state_file_number = fake.unique.random_number(digits=9)
        database_data.append([
            entry["child_last_name"], entry["child_first_name"], entry["child_middle_name"], entry["child_dob"], 
            entry["mom_last_name"], entry["mom_first_name"], state_file_number
        ])

    # Generate unmatched entries
    for _ in range(unmatched_entries):
        if unmatched_target in ["database", "both"]:
            # Add unmatched entry in Database list
            child_last_name = fake.last_name()
            child_first_name = fake.first_name()
            child_middle_name = fake.first_name()
            mom_last_name = fake.last_name()
            mom_first_name = fake.first_name()
            child_dob = generate_child_dob().strftime("%Y-%m-%d")
            state_file_number = fake.unique.random_number(digits=9)
            database_data.append([
                child_last_name, child_first_name, child_middle_name, child_dob, 
                mom_last_name, mom_first_name, state_file_number
            ])

        if unmatched_target in ["medicaid", "both"]:
            # Add unmatched entry in Medicaid list
            mom_first_name = fake.first_name()
            mom_last_name = fake.last_name()
            mom_dob = fake.date_of_birth(minimum_age=18, maximum_age=50).strftime("%Y-%m-%d")
            child_first_name = fake.first_name()
            child_last_name = fake.last_name()
            child_dob = generate_child_dob().strftime("%Y-%m-%d")
            mother_id = fake.unique.random_number(digits=9)
            child_id = fake.unique.random_number(digits=5)
            case_id = fake.unique.random_number(digits=9)
            phone_number = fake.phone_number()
            mobile_number = fake.phone_number()
            street = fake.street_address()
            city = fake.city()
            state = "UT"
            zip_code = fake.zipcode()
            county = "Utah County"
            tobacco_usage = fake.boolean(chance_of_getting_true=10)
            utah_first_time_man = fake.boolean(chance_of_getting_true=20)
            medicaid_data.append([
                mom_first_name, mom_last_name, mom_dob, mother_id, child_id, child_dob, 
                case_id, phone_number, mobile_number, street, city, state, zip_code, 
                county, tobacco_usage, utah_first_time_man
            ])
    
    return (
        pd.DataFrame(database_data, columns=[
            "Child Last Name", "Child First Name", "Child Middle Name", "DOB", 
            "Mother Last Name", "Mother First Name", "State File Number"
        ]),
        pd.DataFrame(medicaid_data, columns=[
            "Mother First Name", "Last Name", "Mother DOB", "Mother ID", "Child ID", "Child DOB", 
            "Case ID", "Phone #", "Mobile #", "Street", "City", "State", "ZIP", 
            "County", "Tobacco Usage", "Utah First Time Man."
        ])
    )

# Function to verify that all names are present in both sheets
def verify_names(database_file, medicaid_data_file):
    database_df = pd.read_excel(database_file)
    medicaid_df = pd.read_excel(medicaid_data_file)
    
    database_names = set(database_df["Mother First Name"] + " " + database_df["Mother Last Name"])
    medicaid_names = set(medicaid_df["Mother First Name"] + " " + medicaid_df["Last Name"])
    
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
    # Prompt for the amount of names to generate
    names_count = int(input("How many names to generate in each list? "))
    # Prompt for unmatched data
    add_unmatched = input("Generate unmatched data? (y/n): ").strip().lower()
    unmatched_entries = 0
    unmatched_target = "both"
    if add_unmatched == 'y':
        unmatched_entries = int(input("Enter the number of unmatched entries: "))
        unmatched_target = input("Add unmatched entries to (database/medicaid/both): ").strip().lower()

    # Generate shared names and DOBs
    shared_data = generate_shared_data(names_count)

    # Generate data for both sheets using the shared data
    database_data_df, medicaid_data_df = generate_medicaid_data(shared_data, unmatched_entries, unmatched_target)

    # Save the data to Excel files
    database_filename = "database_data.xlsx"
    medicaid_data_filename = "medicaid_data.xlsx"
    
    database_data_df.to_excel(database_filename, index=False)
    medicaid_data_df.to_excel(medicaid_data_filename, index=False)
    
    print(f"Files created: {database_filename}, {medicaid_data_filename}")
    
    # Verify that all names are present in both files
    verify_names(database_filename, medicaid_data_filename)

# Run the program
if __name__ == "__main__":
    generate_excel_files()
