import sqlite3
import os


class Pin:
    def __init__(self):

        try:
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, "../database.db")
            self.conn = sqlite3.connect(filename)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def get_room_pins(self, pin_no=None):
        """ Get list of all un-assigned pins from
            pin table.
        """
        cur = self.conn.cursor()
        tuples = None

        try:
            # This is the qmark style:
            if pin_no:
                cur.execute(
                    "SELECT pin_no FROM pin where pin_no not in (select gpio_pin from room where gpio_pin!=:pin_no) and enable = 1 order by pin_no",
                    {"pin_no": pin_no},
                )
            else:
                cur.execute(
                    "SELECT pin_no FROM pin where pin_no not in (select gpio_pin from room) and enable = 1 order by pin_no"
                )
            tuples = cur.fetchall()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return tuples

    def get_pins(self):
        """ Get list of all un-assigned pins from
            pin table.
        """
        cur = self.conn.cursor()
        tuples = None

        try:
            # This is the qmark style:
            cur.execute("SELECT pin_no FROM pin where enable = 1 order by pin_no")
            tuples = cur.fetchall()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return tuples
