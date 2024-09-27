import pandas as pd
from faker import Faker

# Initialize Faker instance
fake = Faker()

# Function to generate random data for children's information
def generate_child_data(num_entries=200):
    child_data = []
    names = []
    for _ in range(num_entries):
        name = fake.first_name() + " " + fake.last_name()
        names.append(name)
        address = fake.address()
        birth_date = fake.date_of_birth(minimum_age=0, maximum_age=18).strftime("%Y-%m-%d")
        ssn = fake.ssn()
        child_data.append([name, address, birth_date, ssn])
    return pd.DataFrame(child_data, columns=["Child Name", "Address", "Birth Date", "SSN"]), names

# Function to generate random data for Medicaid information
def generate_medicaid_data(names, num_entries=200):
    medicaid_data = []
    for i in range(num_entries):
        medicaid_id = fake.unique.random_number(digits=9)
        mom_name = fake.first_name() + " " + fake.last_name()
        birth_date = fake.date_of_birth(minimum_age=0, maximum_age=18).strftime("%Y-%m-%d")
        child_name = names[i]  # Use the same child name from the first sheet
        medicaid_data.append([medicaid_id, mom_name, birth_date, child_name])
    return pd.DataFrame(medicaid_data, columns=["Medicaid ID", "Mom Name", "Child Birth Date", "Child Name"])

# Function to verify that all names are present in both sheets
def verify_names(child_data_file, medicaid_data_file):
    # Load the two Excel files
    child_df = pd.read_excel(child_data_file)
    medicaid_df = pd.read_excel(medicaid_data_file)
    
    # Extract the names from both DataFrames
    child_names = set(child_df["Child Name"])
    medicaid_names = set(medicaid_df["Child Name"])
    
    # Check for missing or extra names
    missing_in_medicaid = child_names - medicaid_names
    missing_in_children = medicaid_names - child_names
    
    if not missing_in_medicaid and not missing_in_children:
        print("All names match in both sheets! No missing or extra names.")
    else:
        if missing_in_medicaid:
            print("Names in children data but missing in Medicaid data:", missing_in_medicaid)
        if missing_in_children:
            print("Names in Medicaid data but missing in children data:", missing_in_children)

# Main function to generate the files
def generate_excel_files():
    # Generate two DataFrames with 200 entries each
    child_data_df, child_names = generate_child_data(200)
    medicaid_data_df = generate_medicaid_data(child_names, 200)

    # Save the data to Excel files
    child_data_filename = "children_data_200.xlsx"
    medicaid_data_filename = "medicaid_data_200.xlsx"
    
    child_data_df.to_excel(child_data_filename, index=False)
    medicaid_data_df.to_excel(medicaid_data_filename, index=False)
    
    print(f"Files created: {child_data_filename}, {medicaid_data_filename}")
    
    # Verify that all names are present in both files
    verify_names(child_data_filename, medicaid_data_filename)

# Run the program
if __name__ == "__main__":
    generate_excel_files()
