# Excel Data Combiner Application

The Excel Data Combiner Application is a user-friendly GUI-based tool designed to merge data from two Excel files—typically hospital and Medicaid datasets—into a unified dataset. It enables users to search, filter, and inspect profiles, view unmatched data, assign nurses, and analyze nurse statistics. With additional features like encryption and decryption, it ensures secure handling of sensitive information.

## Features
- - **Read Two Excel Files:** Load hospital and Medicaid datasets for merging.
- - **Combine Data:** Merge datasets based on Mother's First Name, Last Name, and Child's Date of Birth.
- - **Search & Filter:** Search and filter combined data by name, ID, or Date of Birth.
- - **View Detailed Profiles:** Double-click an entry to view detailed information, including mother and child details.
- - **Copy to Clipboard:** Copy profile details for documentation and sharing.
- - **Excel Export:** Save the combined dataset as `combined_matched_data.xlsx`.
- - **Unmatched Data Inspection:** View and explore unmatched data records.
- - **Nurse Assignment:** Assign nurses to children and manage nurse statistics.
- - **Nurse Statistics:** Analyze assigned nurses, view most/least assigned nurses, and inspect their assigned children.
- - **Encryption & Decryption:** Encrypt and decrypt Excel files automatically for added security.
- - **Generate Encryption Key:** Generate a key to secure data files.
- - **Detailed Logging:** Track application activity for operational insights.

## Prerequisites

Ensure the following requirements are met to run the application:

- **Python 3.x** installed.
- Required Python Libraries:
- - `pandas`
- - `tkinter`
- - `openpyxl`
- - `logging`
- - `reportlab`
- - `cryptography`
- - `platform`
- - `app_crypto`

You can install the required dependencies using pip:
``` bash
pip install pandas openpyxl tkinter reportlab cryptography
```

## Installation

1. Clone or download this repository.
2. Ensure the required Python packages are installed (see above).
3. Place your two Excel files (hospital and Medicaid datasets) in an accessible location.

## Usage

1. Run the `app.py` script:

``` bash
python app.py
```

2. The GUI will open with buttons to:
- - **Read Excel File 1:** Load the first dataset (e.g., hospital data).
- - **Read Excel File 2:** Load the second dataset (e.g., Medicaid data).
- - **Combine Data:** Merge the datasets for analysis.
- - **Search & Filter:** Search entries by Mother ID, Child Name, or Date of Birth.
- - **View Profile:** Double-click an entry to view detailed information.
- - **Unmatched Data:** Inspect unmatched data records.
- - **Nurse Assignment:** Assign nurses to children and analyze nurse-related statistics.
- - **View Nurse Statistics:** View assigned nurses and statistics about them.
- - **Generate Report:** Generate statistical report about children and nurses (with an ability to export in pdf).

## Application Workflow

- **Read Excel Files:** Click the "Read Excel File" buttons to load two Excel files (hospital and Medicaid datasets).
- **Combine Data:** After loading both files, click "Combine Data" to merge the files based on "Mother’s First Name," "Mother’s Last Name," and "Child’s Date of Birth."
- **Search & Filter:** Use the search bar to filter the displayed names.
- **View Profiles:** Double-click an entry to view a detailed profile.
- **Copy Profile Info:** Copy profile details to the clipboard by clicking the "Copy Profile Info" button.
- **Analyze Nurse Statistics:** View detailed statistics on nurse assignments.

## Application Layout  

### Main Window

- **Read Excel File 1:** Opens a file dialog for selecting the first Excel file.
- **Read Excel File 2:** Opens a file dialog for selecting the second Excel file.
- **Combine Data:** Merges the two datasets.

### Combined Data Window

- **Search Bar:** Filter entries by Mother ID, Child Name, or Child DOB.
- **Results List:** Displays "Mother ID," "Child Name," and "Child DOB."
- **Double-click Feature:** Opens a detailed profile for the selected entry.

### Profile View

Displays detailed information including:

- **Mother’s Information:** Mother ID, First Name, Last Name.
- **Child’s Information:** First Name, Last Name, Date of Birth.
- **Contact Information:** Street Address, City, State, ZIP, Phone, and Mobile Number.
- **Copy Profile Info:** Copies the profile details to the clipboard.
- **Assign Nurse:** Asks for a name to assign a nurse to the child.

### Unmatched Data Window
Includes unmatched data with origin specified and an ability to view the details in a drop down format. 

### Nurse Statistics Window
- **Most Assigned Nurse:** Displays the name of the most assigned nurse.
- **Least Assigned Nurse:** Displays the name of the least assigned nurse.
- **Clickable Nurse Names:** Display assigned children to specific nurse and their profiles.

## Logging
The application logs key events such as file reading, data combination, and errors. These logs are displayed in the console.

- **INFO:** Successful operations.
- **WARNING:** Operations that did not complete as expected (e.g., no file selected).
- **ERROR:** Issues encountered (e.g., data combination errors).

## Excel File Output
- **Combined Data:** is saved as `combined_matched_data.xlsx` in the current working directory after successfully combining the two datasets.
- **Unmatched Data:** Saved as unmatched_data.xlsx for records that couldn't be matched during merging.

## Unit Testing
The application includes a set of unit tests using the `unittest` or `pytest` module to ensure the functionality of critical features:

- **Test for Reading Excel Files:** Simulates reading an Excel file and verifies if the data is correctly loaded and appended.
- **Test for Data Combination:** Ensures that the two datasets are merged correctly based on "Mother’s Name" and "Child’s Date of Birth."
- **Test for Excel File Generation:** Verifies that the combined data is saved to an Excel file named `combined_matched_data.xlsx`.  

You can run the tests using `pytest` with rich formatting for enhanced readability:

``` bash
pytest --rich --tb=short -v test.py
```

## Changes
- **New GUI Components:** Updated the GUI with a modern layout using ttk.Treeview for better data visualization.
- **New Copy Functionality:** Added functionality to copy profile information to the clipboard.
- **Unit Test Integration:** Introduced unit tests using unittest for testing key functions like reading Excel files, data combination, and Excel file generation.
- **Enhanced Logging:** Added detailed logging for tracking successful operations, warnings, and errors, visible in the console.
- **Improved Data Normalization:** Enhanced the data merging process by normalizing names and standardizing date formats.
- **Error Handling:** Implemented better error handling for file operations and merging errors.
- **Nurse Assignment:** Assign and analyze nurse assignments.
- **Security Features:** File encryption and decryption for added data protection.
- **Report Generation:** Generates a report containing nurse data and children data statistics.
