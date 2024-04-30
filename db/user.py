import sqlite3
import os


class User:
    def __init__(self):

        try:
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, "../database.db")
            self.conn = sqlite3.connect(filename)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

    def get_users(self):
        """ Get list of all users from
            user table.
        """
        cur = self.conn.cursor()
        tuples = None

        try:
            # This is the qmark style:
            cur.execute(
                "SELECT user.id, user.name, room.name as room, CASE registered WHEN 1 THEN 'Yes' ELSE 'No' END Register FROM user LEFT JOIN room ON user.room_id = room.id order by user.id"
            )
            tuples = cur.fetchall()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return tuples

    def get_user(self, id):
        """ Get list of all users from
            user table.
        """
        cur = self.conn.cursor()
        tuples = None

        try:
            # This is the qmark style:
            cur.execute(
                "SELECT id, name, room_id, registered FROM user where id = :id",
                {"id": id},
            )
            tuples = cur.fetchone()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return tuples

    def get_user_room_pin(self, user_id):
        """ Get list of all users from
            user table.
        """
        cur = self.conn.cursor()
        tuples = None

        try:
            # This is the qmark style:
            cur.execute(
                "SELECT room.gpio_pin FROM user LEFT JOIN room ON user.room_id=room.id  where user.id = :id",
                {"id": user_id},
            )
            tuples = cur.fetchone()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return tuples

    def get_user_by_room(self, room_id):
        """ Get list of all users from
            user table.
        """
        cur = self.conn.cursor()
        tuples = None

        try:
            # This is the qmark style:
            cur.execute(
                "SELECT id, name, room_id, registered FROM user where room_id = :room_id",
                {"room_id": room_id},
            )
            tuples = cur.fetchone()
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return tuples

    def add_user(self, name, room_id):
        """ Add a new user in the database
            user table.
        """
        try:
            cur = self.conn.cursor()

            cur.execute(
                "INSERT into user(name,registered,room_id) VALUES(:name,0,:room_id)",
                {"name": name, "room_id": room_id},
            )
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return False

    def update_user(self, id, name, room_id):
        """ Update user room in the database
            user table, after succefull training.
        """
        try:
            cur = self.conn.cursor()

            cur.execute(
                "UPDATE user SET name=:name, room_id=:room_id WHERE id=:id",
                {"id": id, "name": name, "room_id": room_id},
            )
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return False

    def delete_user(self, id):
        """ Delete a user in the database
            user table.
        """
        try:
            cur = self.conn.cursor()

            cur.execute(
                "DELETE FROM user WHERE id=:id", {"id": id},
            )
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return False

    def register_user(self, id):
        """ Mark a user in the database
            user table, after succefull training.
        """
        try:
            cur = self.conn.cursor()

            cur.execute(
                "UPDATE user SET registered=1 WHERE id=:id", {"id": id},
            )
            self.conn.commit()
            self.conn.close()
            return True
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return False
