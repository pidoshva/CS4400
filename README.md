## Features

- **Read Two Excel Files**: The application reads two Excel files, typically containing different types of data, and merges them based on the "Mother ID", "Mother Name", and "Child's Date of Birth".
- **Combine Data**: Combines the two datasets into a single dataset for further inspection.
- **Search & Filter**: Users can search and filter combined data for quick access.
- **Display Profiles**: Double-clicking on a name displays detailed profile information for the selected entry.
- **Copy to Clipboard**: The profile information can be copied to the clipboard for easy sharing or documentation.

## Prerequisites

To run this application, you need:

- Python 3.x installed.
- The following Python libraries:
  - `pandas`
  - `tkinter`
  - `openpyxl` (for handling `.xlsx` files)
  - `logging`

You can install the required dependencies using pip:

```bash
pip install pandas openpyxl
```
## Installation  
1. Clone or download this repository.  
2. Ensure the required Python packages are installed (see above).
3.  Place your two Excel files (hospital and Medicaid datasets) in a location where they can be accessed.  

## Usage  
1. Run the `app.py` script:  
``` bash
python app.py
```

2. The graphical user interface (GUI) will open, and you will see buttons to:  

- Read Excel File 1: Use this to load the hospital data.
- Read Excel File 2: Use this to load the Medicaid data.
- Combine Data: After loading both files, click this button to merge the datasets.  

3. After merging, a new window will display a list of combined child records, showing the Mother ID, Child Name, and DOB.

4. View Child Profile: Double-click on any entry in the list to open a new window displaying the full profile of the child, including all data from both the hospital and Medicaid records.

5. The merged data is saved as `combined_matched_data.xlsx`, and unmatched data will be logged in the console.

## Application Workflow
- **Read Excel Files**: Click the buttons `Read Excel File 1` and `Read Excel File 2` to load two Excel files for merging.
- **Combine Data**: Once both Excel files are loaded, click "Combine Data" to merge them based on the common fields.
- **Search & Filte**r: After combining, you can search for specific entries using the search bar in the new window.
- **View Profiles**: Double-clicking an entry from the results list will show a detailed profile view of the individual entry.
- **Copy Profile Info**: You can copy the profile information to the clipboard by clicking the "Copy Profile Info" button.

## Application Layout
### Main Window
The main window contains three primary buttons:

- **Read Excel File 1**: Opens a file dialog to select the first Excel file.
- **Read Excel File 2**: Opens a file dialog to select the second Excel file.
- **Combine Data**: Combines the data from both files based on matching fields.
### Combined Data Window
Once the data is combined, a new window appears displaying the merged entries. It includes:

- **Search Bar**: Allows you to filter through the entries by name, ID, or date of birth.
- **Results List**: Shows the "Mother ID", "Child Name", and "Child DOB" in a structured format.
- **Double-click Feature**: Double-clicking on a result opens a detailed profile of that entry.
### Profile View
When an entry is double-clicked, a profile window displays more detailed information, such as:

- **Mother's Information**: Mother ID, first name, and last name.
- **Child's Information**: Child's first name, last name, and date of birth.
- **Address and Contact**: Address, phone number, and mobile number (if available).
- **Copy Profile Info**: A button to copy all profile details to the clipboard in a well-organized format.

## Logging  
The application logs key events such as file reading, data combination, search activities, and errors to the console. This makes it easier to debug or track the application's activity.

**INFO**: Information messages for successful operations.  
**ERROR**: Error messages for any issues that occur.
Logs are displayed in the console output and help you track the application's behavior.

