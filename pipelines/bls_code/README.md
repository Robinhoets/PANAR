BLS Data Retrieval

This code fetches economic data from the BLS API, cleans it, and produces separate JSON files for each data series. Each JSON contains:
* Title: Data point label
* Dates: Formatted as “Month Year”
* Values: Corresponding numeric values

Setup & Installation
1. Create and Activate Environment:
    - conda create --name myenv python=3.9 mkl numpy pandas
    - conda activate myenv
2. Install Requests:
    - pip install requests
3. Configure the Script:
    - Save the script as bls_data_retrieval.py.

Running the Script

In your terminal, navigate to the project directory and run:

- python bls_data_retrieval.py

The script will:
* Retrieve data in 20-year chunks (from 1970 to 2023).
* Clean and merge the data.
* Generate individual JSON files for each series

Output
* A combined DataFrame is printed to the console.
* Separate JSON files are created in the project folder (e.g., civilian_labor_force_(sa).json, etc.).
