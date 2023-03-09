
  
  

# AZC Camp Locations Tool (For PostgreSQL Testing)

  ![enter image description here](https://user-images.githubusercontent.com/122477951/224136310-6605add7-403d-4d1a-a82b-20fe84996f7b.png)

This Python tool is designed to scrape coa.nl website and find the current refugee camp locations and save the data in a PostgreSQL database.

  

## Database structure

![With 1 to many](https://user-images.githubusercontent.com/122477951/224125267-74d322ec-b125-4947-aa1e-53fa9d53edd5.png)

  
  

(the ERD diagram was created by pgadmin4)

  

There are 2 tables, **`AZCs`** and **`Location_Details`** with the **primary key** for both being `id` (a serial).

  

There is a **one-to-many** link between the table `AZCs` and `Location_Details`.

  

Both tables have a **foreign key**; `id`. For more details, see the **sql.txt** file.

  
  
  

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

  

To create the required tables in the database, you need to execute the SQL commands in the **`sql.txt`** file. You can do this by running the following command:

  
  

psql -U username -d database_name -f sql.txt

  

Replace username and database_name with your own values.

  

You also need to create a "**`database.ini`**" file which contains the following:

  

[postgresql]

  

host=localhost

database=database_name_here

user=user_name_here

password=password_here

  
  
  

## Usage

  

  

Run the main.py file by typing the following command in your terminal:

  

python3 main.py

  

This will open the tool's graphical user interface (GUI), where you can perform web scraping, save the data from coa's website and also you can empty the tables.

  
  
  
  
  
  

## License

  

This project is licensed under the MIT License.
