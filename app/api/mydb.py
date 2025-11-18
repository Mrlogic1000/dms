from ..extensions import mysql

class MySQLCRUD:
    def __init__(self ):
        self.conn = mysql.connection
        self.cursor = mysql.connection.cursor()
        # self.cursor = self.conn.cursor()

    def create(self, table, data):
        """Inserts a new record into the specified table."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.Error as e:
            self.conn.rollback()
            print(f"Error creating record: {e}")
            return None

    def read(self, table, conditions=None, columns='*'):
        """Retrieves records from the specified table."""
        sql = f"SELECT {columns} FROM {table}"
        if conditions:
            where_clause = ' AND '.join([f"{col} = %s" for col in conditions.keys()])
            sql += f" WHERE {where_clause}"
            self.cursor.execute(sql, tuple(conditions.values()))
        else:
            self.cursor.execute(sql)
        if conditions:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

        

    def update(self, table, data, conditions):
        """Updates existing records in the specified table."""
        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
        where_clause = ' AND '.join([f"{col} = %s" for col in conditions.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        values = tuple(data.values()) + tuple(conditions.values())
       
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            return self.cursor.rowcount
        except mysql.Error as e:
            self.conn.rollback()
            print(f"Error updating record: {e}")
            return None

    def delete(self, table, conditions):
        """Deletes records from the specified table."""
        where_clause = ' AND '.join([f"{col} = %s" for col in conditions.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        try:
            self.cursor.execute(sql, tuple(conditions.values()))
            self.conn.commit()
            return self.cursor.rowcount
        except mysql.Error as e:
            self.conn.rollback()
            print(f"Error deleting record: {e}")
            return None

    def close(self):
        """Closes the database connection."""
        self.cursor.close()
       
    

# Example Usage:
# if __name__ == "__main__":
#     db_crud = MySQLCRUD("localhost", "root", "your_password", "your_database")

    # Create
    # new_user_id = db_crud.create("users", {"name": "Alice", "email": "alice@example.com"})
    # if new_user_id:
    #     print(f"New user created with ID: {new_user_id}")

    # Read
    # users = db_crud.read("users", conditions={"name": "Alice"})
    # print("Users named Alice:", users)

    # Update
    # updated_rows = db_crud.update("users", {"email": "alice.smith@example.com"}, {"name": "Alice"})
    # print(f"Updated {updated_rows} rows.")

    # Delete
    # deleted_rows = db_crud.delete("users", {"name": "Alice"})
    # print(f"Deleted {deleted_rows} rows.")

    # db_crud.close()