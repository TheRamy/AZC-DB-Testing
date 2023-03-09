from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
import sys
import psycopg2


from fetch import *
from config import config


global AppTitle
AppTitle = "AZC Camp Locations Tool (For PostgreSQL Testing)"


class MainUI(QDialog):
    def __init__(self):
        super(MainUI, self).__init__()
        loadUi("./UI/main.ui", self)

        self.buttonfetchAZCLocations.clicked.connect(self.AZC_fetchList)
        self.buttonEmptyTables.clicked.connect(self.emptyTables)

        self.AZCs.currentTextChanged.connect(self.showTableOneAndTwo)

    def emptyTables(self):

        if self.show_popupYesNo("Are you sure you want to empty the tables of any data?") is True:
            try:

                # read connection parameters
                params = config()

                # connect to the PostgreSQL server
                print('Connecting to the PostgreSQL database...')
                conn = psycopg2.connect(**params)
                # create a cursor
                cur = conn.cursor()

                # Truncate the "AZCs" table
                cur.execute("TRUNCATE TABLE \"AZCs\" CASCADE;")
                # Truncate the "Location_Details" table
                cur.execute("TRUNCATE TABLE \"Location_Details\" CASCADE;")
                # Commit the changes to the database
                conn.commit()
                self.show_popup(
                    "Tables emptied! The app will close! Please restart!")
                app.quit()

            except (Exception, psycopg2.Error) as error:
                print("error: ", error)

            finally:
                # closing database connection.
                if conn:
                    cur.close()
                    conn.close()
                    print("PostgreSQL connection is closed")

    def AZC_fetchList(self):

        try:

            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            # create a cursor
            cur = conn.cursor()

            # Query the "AZCs" table
            cur.execute("SELECT * FROM \"AZCs\"")

            # Fetch all items
            items = cur.fetchall()

            # Check if the result is empty
            if len(items) == 0:

                if self.show_popupYesNo("Tables are empty, do you want to fetch fresh data from www.COA.nl?") is True:

                    insert_AZC_records()
                    insert_More_AZC_records()

                    self.show_popup("Data added! Please restart the app!")
                    app.quit()

            else:

                #  list the AZC_Names
                for azc in items:
                    # print(azc[0])
                    self.AZCs.addItem(azc[1])

                self.buttonfetchAZCLocations.setEnabled(False)

        except (Exception, psycopg2.Error) as error:
            print("error: ", error)

        finally:
            # closing database connection.
            if conn:
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")

    def showTableOneAndTwo(self):

        choosen_AZC = str(self.AZCs.currentItem().text())

        try:

            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            # create a cursor
            cur = conn.cursor()

            # search for a specific AZC_Name and retrieve all
            cur.execute(
                "SELECT * FROM \"AZCs\" WHERE \"AZC_Name\" = %s", (choosen_AZC,))

            item = cur.fetchone()

            azc_id = item[0]
            azc_name = item[1]
            azc_link = item[2]

            # print (azc_id, azc_name, azc_link)

            self.idLabel.setText(str(azc_id))
            self.locationNameLabel.setText(str(azc_name))
            self.LinkLabel.setText(str(azc_link))

            # using the id, search the second table
            cur.execute(
                "SELECT * FROM \"Location_Details\" WHERE id = %s", (azc_id,))

            second_item = cur.fetchone()

            second_id = second_item[0]
            second_postal_code = second_item[1]
            second_house_number = second_item[2]
            second_location_manager = second_item[3]

            self.idsecondLabel.setText(str(second_id))
            self.PostalCodeLabel.setText(str(second_postal_code))
            self.HouseNumberLabel.setText(str(second_house_number))
            self.LocationManagerLabel.setText(str(second_location_manager))

        except (Exception, psycopg2.Error) as error:
            print("error: ", error)

        finally:
            # closing database connection.
            if conn:
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")

    def show_popup(self, txt):
        # Create and show the popup message

        msg = QMessageBox()
        msg.setText(txt)
        msg.setWindowTitle(AppTitle)
        msg.exec_()

    def show_popupYesNo(self, txt):
        # Create and show the popup message
        msg = QMessageBox()
        msg.setText(txt)
        msg.setWindowTitle(AppTitle)

        # Add buttons for yes or no
        yes_button = msg.addButton(QMessageBox.Yes)
        no_button = msg.addButton(QMessageBox.No)

        # Set the default button to be "No"
        msg.setDefaultButton(no_button)

        # Execute the popup message and check the user's choice
        choice = msg.exec_()
        if choice == QMessageBox.Yes:
            return True  # print("YESSSSSSSSSSes")
        elif choice == QMessageBox.No:
            return False  # print("NOOOOOOOOO")


app = QtWidgets.QApplication(sys.argv)
UI = MainUI()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UI)
widget.setFixedWidth(738)  # 800
widget.setFixedHeight(253)  # 600
widget.setWindowTitle(AppTitle)

# Center the app on the screen
screen_resolution = app.desktop().screenGeometry()
widget.setGeometry(screen_resolution.width() // 2 - widget.width() // 2,
                   screen_resolution.height() // 2 - widget.height() // 2,
                   widget.width(), widget.height())

widget.show()
sys.exit(app.exec_())
