import sqlite3
import os


class Room:
    def __init__(self):

        try:
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, "../database.db")
            self.conn = sqlite3.connect(filename)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def get_rooms(self):
        """ Get list of all rooms from
            room table.
        """
        cur = self.conn.cursor()
        tuples = None

        try:
            # This is the qmark style:
            cur.execute("SELECT id, name, gpio_pin, common FROM room")
            tuples = cur.fetchall()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return tuples

    def get_room(self, id):
        """ Get list of all users from
            user table.
        """
        cur = self.conn.cursor()
        tuples = None

        try:
            # This is the qmark style:
            cur.execute(
                "SELECT id, name, common, gpio_pin FROM room where id = :id",
                {"id": id},
            )
            tuples = cur.fetchone()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return tuples

    def get_common_room_pins(self):
        """ Get list of all users from
            user table.
        """
        cur = self.conn.cursor()
        tuples = None

        try:
            # This is the qmark style:
            cur.execute("SELECT gpio_pin FROM room where common=1")
            tuples = cur.fetchall()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return tuples

    def add_room(self, name, gpio_pin, common=False):
        """ Add a new room in the database
            room table.
        """
        try:
            cur = self.conn.cursor()

            cur.execute(
                "INSERT into room(name, common, gpio_pin) VALUES(:name,:common,:gpio_pin)",
                {"name": name, "common": common, "gpio_pin": gpio_pin},
            )
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return False

    def get_user_room(self, room_id=None):
        """ Get list of rooms available for 
            user.
        """
        cur = self.conn.cursor()
        tuples = None

        try:
            # This is the qmark style:
            if room_id:
                cur.execute(
                    "SELECT id, name FROM room where id not in (SELECT room_id FROM user where room_id != :room_id) and common = 0",
                    {"room_id": room_id},
                )
            else:
                cur.execute(
                    "SELECT id, name FROM room where id not in (SELECT room_id FROM user) and common = 0"
                )
            tuples = cur.fetchall()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return tuples

    def delete_room(self, id):
        """ Delete a room in the database
            room table.
        """
        try:
            cur = self.conn.cursor()

            cur.execute(
                "DELETE FROM room WHERE id=:id", {"id": id,},
            )
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return False

    def update_room(self, id, name, gpio_pin, common=False):
        """ Update room in the database
            room table.
        """
        try:
            cur = self.conn.cursor()

            cur.execute(
                "UPDATE room SET name=:name, gpio_pin=:gpio_pin, common=:common WHERE id=:id",
                {"id": id, "name": name, "gpio_pin": gpio_pin, "common": common},
            )
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return False
