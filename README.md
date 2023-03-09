
# AZC Camp Locations Tool (For PostgreSQL Testing)

  
This Python tool is designed to scrape coa.nl website and find the current refugee camp locations and save the data in a PostgreSQL database. 



## Requirements


 1. Python 3.6 or higher
 2. pip package installer
 3. beautifulsoup4 library for web scraping
 4. PyQt5 5.15.9
 5. requests 2.25.1 or higher

## Installation

  

Clone or download the repository to your local machine.
Navigate to the project directory in your terminal / command prompt.
Install the required packages by running the following command:

    pip install -r requirements.txt

To create the required tables in the database, you need to execute the SQL commands in the sql.txt file. You can do this by running the following command:


    psql -U username -d database_name -f sql.txt

Replace username and database_name with your own values.

You also need to create a "database.ini" file which contains the following:

    [postgresql] 

    host=localhost
    database=azc_locations 
    user=db_ramy 
    password=db_ramy



## Usage

  

Run the main.py file by typing the following command in your terminal:

    python3 main.py

This will open the tool's graphical user interface (GUI), where you can perform web scraping, save the data from coa's website and also you can empty the tables.




## License

  This project is licensed under the MIT License.
