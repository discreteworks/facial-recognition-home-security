import sqlite3
import hashlib
import os


class Admin:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "../database.db")
        self.conn = sqlite3.connect(filename)

    def update_password(self, old, new):
        """ Update password.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(
                "SELECT login FROM admin WHERE login = :login and password = :password",
                {"login": "admin", "password": hashlib.md5(old.encode()).hexdigest()},
            )
            if cur.fetchone():
                hash_object = hashlib.md5(new.encode())
                md5_hash = hash_object.hexdigest()
                cur.execute(
                    "UPDATE admin SET password=:password WHERE login='admin'",
                    {"password": md5_hash},
                )
                self.conn.commit()
                self.conn.close()
                return True
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return False

    def authenticate(self, login, password):
        """ Authenticate user.
        """
        cur = self.conn.cursor()

        hash_object = hashlib.md5(password.encode())

        md5_hash = hash_object.hexdigest()

        try:
            # This is the qmark style:
            cur.execute(
                "SELECT login FROM admin WHERE login = :login and password = :password",
                {"login": login, "password": md5_hash},
            )

            if cur.fetchone():
                self.conn.close()
                return True

        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

        self.conn.close()
        return False
