# Nurse Filter Prototype

## Overview

This prototype is designed to combine two Excel datasets: one containing hospital data of children and their birth information, and the other containing Medicaid data. The two datasets are merged based on **Mother's First Name**, **Mother's Last Name**, and **Child's Date of Birth (DOB)**.

The program then displays the combined data in a graphical user interface (GUI) where the user can see the merged list of children. By selecting a child from the list, users can view their detailed profile, which is compiled from both the hospital and Medicaid data.

## Features

- **Read two Excel files**: The program reads hospital and Medicaid data from two separate Excel files.
- **Merge the datasets**: The program merges the two datasets based on three key fields:
  - **Mother's First Name**
  - **Mother's Last Name**
  - **Child's Date of Birth**
- **Display combined data**: The merged data is displayed in a listbox, showing each child's **Mother ID**, **Child Name**, and **DOB**.
- **Child profile view**: Double-clicking a child in the listbox opens a detailed view of the child’s profile, which includes all combined information.
- **Output of unmatched data**: Any rows from the original datasets that do not have matching records are logged in the console as "Unmatched" with their Mother IDs.

## Requirements

- Python 3.7 or higher
- The following Python packages:
  - `pandas`
  - `tkinter`
  - `openpyxl` (to handle Excel files)

You can install the required packages using `pip`:

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

5. The merged data is saved as combined_matched_data.xlsx, and unmatched data will be logged in the console.

## Data Fields  
### Expected Columns in the Hospital Dataset:
- Mother_First_Name
- Mother_Last_Name
- DOB (Date of Birth of the child)
- Additional information such as the child’s name, state file number, etc.  

### Expected Columns in the Medicaid Dataset:
- Mother_First_Name
- Last_Name (Mother’s Last Name)
- Child_DOB
- Additional information such as Medicaid ID, phone numbers, addresses, etc.
## Handling Errors  

- If the Excel files are not in the expected format (e.g., missing key columns like Mother_First_Name or Child_DOB), the program will raise an error.
- Ensure that both Excel files have consistent data formats before running the merge operation.
