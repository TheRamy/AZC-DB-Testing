from bs4 import BeautifulSoup
import psycopg2
import requests
from config import config


def fetchData():

    url = "https://www.coa.nl/nl/locatiezoeker"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    select_box = soup.find("select", {"id": "1109--type"})
    options = select_box.find_all("option")

    locations = {}
    for option in options:
        locations[option.text] = option["value"]

    azcLocationNames = []
    azcLocationLinks = []

    Limit = 20
    n = 0

    for LocationName, LocationLink in locations.items():
        if LocationLink != "" and n <= Limit:

            # print(location, link)

            azcLocationNames.append(LocationName)
            azcLocationLinks.append(LocationLink)
            n += 1

    # azc_fetchLocations()[0] is a list of location names
    # azc_fetchLocations()[1] is a list of location links
    return azcLocationNames, azcLocationLinks


def fetchMoreData(url):

    # url = "https://www.coa.nl/nl/locatie/arnhem-velperweg"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    ##################################
    # find house number
    ##################################
    address_item = soup.find_all(
        'li', class_='quickContact__addressItem')[0]
    address = address_item.text

    house_number = [int(x) for x in address.split() if x.isdigit()]
    if len(house_number) > 0:
        house_number = house_number[0]
    else:
        print("Index house_number out of range")

    ##################################
    # find postal code
    ##################################
    postalCode_item = soup.find_all(
        'li', class_='quickContact__addressItem')[1]
    postalCode = postalCode_item.text
    postalCode = postalCode.replace(' ', '')
    postalCode = postalCode[:6]

    ###################################
    # find location manager
    ###################################

    Locatiemanager = soup.find(
        'section', {'class': 'richText'}).find('p').text.strip()
    Locatiemanager = Locatiemanager.replace('De locatiemanager is ', '')
    Locatiemanager = Locatiemanager.replace('De locatiemanager is', '')
    Locatiemanager = Locatiemanager.replace('Locatiemanager:', '')

    Locatiemanager = Locatiemanager.replace('De manager is', '')
    Locatiemanager = Locatiemanager.replace('De manager amv is', '')
    Locatiemanager = Locatiemanager.replace('Manager AMV is', '')

    Locatiemanager = Locatiemanager.replace('.', '')
    Locatiemanager = Locatiemanager.replace(':', '')

    addressInfo = []

    addressInfo.append(postalCode)  # index 0
    addressInfo.append(house_number)  # index 1
    addressInfo.append(Locatiemanager)  # index 2

    # addressInfo[0] is postal code & addressInfo[1] is house number
    return addressInfo


def insert_AZC_records():

    azc_locationNames = fetchData()[0]
    azc_locationLinks = fetchData()[1]

    try:

        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()

        for index in range(len(azc_locationNames)):

            # print (azc_locationNames[index] )
            # print(azc_locationLinks[index])

            # First, check if a record already exists with the given AZC_Name
            postgres_select_query = """SELECT * FROM "AZCs" WHERE "AZC_Name" = %s"""
            cur.execute(postgres_select_query, (azc_locationNames[index],))
            existing_record = cur.fetchone()

            if existing_record:
                # If a record already exists
                print("Record already exists in database: ", existing_record)
            else:
                # If no record found, insert
                postgres_insert_query = """INSERT INTO "AZCs" ("id", "AZC_Name", "AZC_Link") VALUES (%s, %s, %s)"""
                record_to_insert = (
                    index, azc_locationNames[index], azc_locationLinks[index])
                cur.execute(postgres_insert_query, record_to_insert)
                conn.commit()
                print(f"Record no.{index} inserted successfully.")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert records into table", error)

    finally:
        # closing database connection.
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")


def insert_More_AZC_records():

    try:

        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()

        # Execute a SELECT query to retrieve all rows from the AZCs table
        cur.execute("""SELECT id, "AZC_Link" FROM "AZCs" """)

        # Fetch all the rows and add new entries to Location_Details
        rows = cur.fetchall()

        for row in rows:
            id = row[0]

            # Retrieve the AZC_Link value for the current row
            cur.execute(
                """SELECT "AZC_Link" FROM "AZCs" WHERE id = %s""", (id,))
            azc_link = cur.fetchone()[0]
            # print(f"Trying to insert location data for id {id} with {azc_link}")

            fetched = fetchMoreData(azc_link)

            postal_code = fetched[0]
            house_number = fetched[1]
            location_manager = fetched[2]

            # Check if a row with the same id exists in the Location_Details table
            cur.execute(
                """SELECT id FROM "Location_Details" WHERE id = %s""", (id,))
            if cur.fetchone() is None:
                # If the row doesn't exist, insert a new row with the same id

                postgres_insert_query = """INSERT INTO "Location_Details" (id, postal_code, house_number, location_manager) VALUES (%s, %s, %s, %s)"""
                record_to_insert = (
                    id, postal_code, house_number, location_manager)
                cur.execute(postgres_insert_query, record_to_insert)

                conn.commit()
                print(f"#{id} Location details added from {azc_link}")

            else:
                print(f"#{id} Location details already exist for {azc_link}")

    except (Exception, psycopg2.Error) as error:
        print("Connection error: ", error)

    finally:
        # closing database connection.
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")


# This will fetch a list of all AZCs (camps) from COA's website
# and save it into the database
# It will first check if this camp is already in the list or not


#insert_AZC_records()
#insert_More_AZC_records()
