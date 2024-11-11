# Excel Data Combiner Application

This application merges data from two Excel files, typically hospital and Medicaid datasets, into one dataset for further inspection. It allows users to search, filter, view, and copy detailed profiles based on the merged data.

## Features
- **Read Two Excel Files:** Users can select two Excel files (hospital and Medicaid datasets) and merge them based on the Mother’s First Name, Last Name, and Child’s Date of Birth.
- **Combine Data:** Combines the datasets into a single file for easy inspection.
- **Search & Filter:** Quickly search and filter combined data by name, ID, or Date of Birth.
- **Display Profiles:** Double-clicking on a name opens a detailed profile for the selected entry, showing information about the mother, child, and contact details.
- **Copy to Clipboard:** Users can copy profile information for easy documentation and sharing.
- **Excel Export:** Saves the combined dataset to an Excel file (combined_matched_data.xlsx).
- **Unmatched Data:** Displays unmatched data if any found.
- **Nurse Assignment:** Ability to assign nurses to children
- **Nurse Statistics:** Displays every assigned nurse and the amount of children assigned to that nurse with an ability to view children's profiles.
- **Encryption Key Generation:** Generates an encryption key for file encryption.
- **File Encryption/Decryption:** An ability to encrypt and decrypt `xlsx` file for added protection.

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
pip install pandas openpyxl
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
- **Read Excel File 1:** Load the first Excel dataset (e.g., hospital data).
- **Read Excel File 2:** Load the second Excel dataset (e.g., Medicaid data).
- **Combine Data:**  Merge the two datasets based on "Mother’s Name" and "Child’s Date of Birth."

3. After merging, a new window will display the combined records, showing "Mother ID," "Child Name," and "Child DOB."

4. **View Child Profile:** Double-click on an entry to view a detailed profile of the selected entry, including information about the mother, child, and contact details.

5. **Copy Profile Info:** Copy profile details to the clipboard for easy sharing.

## Application Workflow

- **Read Excel Files:** Click the "Read Excel File" buttons to load two Excel files (hospital and Medicaid datasets).
- **Combine Data:** After loading both files, click "Combine Data" to merge the files based on "Mother’s First Name," "Mother’s Last Name," and "Child’s Date of Birth."
- **Search & Filter:** Use the search bar to filter the displayed names.
- **View Profiles:** Double-click an entry to view a detailed profile.
- **Copy Profile Info:** Copy profile details to the clipboard by clicking the "Copy Profile Info" button.

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
The combined dataset is saved as `combined_matched_data.xlsx` in the current working directory after successfully combining the two datasets.

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
