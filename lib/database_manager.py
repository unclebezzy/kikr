# Imports
import sqlite3

class DatabaseManager(object):
    """ Manage SQLite database related operations
    
    Methods:
        __init__() - Connect to the database
        list() - List all bots
        new() - Create a new bot
        modify() - Modify a bot
        delete() - Delete a bot
        info() - Get info on a bot
    """
    
    def __init__(self, db_file):
        """ Connect to the database
        
        Arguments:
            db_file - string - The database to connect to
        """
        
        # Attempt to connect to the database
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            
        except sqlite3.Error as err:
            # Display an error message and exit
            print("[E] Error connecting to database: {}".format(err))
            exit(1)
            
        # Check if the table contacts exists and create if it doesn't
        self.cursor.execute(""" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='chatbots' """)
        
        if self.cursor.fetchone()[0] == 0:
            # Create the contacts table
            self.cursor.execute("""CREATE TABLE chatbots (
                id integer PRIMARY KEY,
                bot_name TEXT,
                username TEXT,
                password TEXT
            )""")
                
            self.conn.commit()
            
    def list(self):
        """ Return a list of all chatbots
        
        Arguments:
            None
        """
        
        # Create and run the query
        sql_query = """ SELECT * FROM chatbots """
        self.cursor.execute(sql_query)
        bot_list = self.cursor.fetchall()
        
        # Return the info
        return bot_list
        
    def new(self, bot_name, username, password):
        """ Create a new bot
        
        Arguments:
            bot_name - string - The name of the bot
            username - string - The Kik username
            password - string - The Kik password
        """
        
        # Create the SQL query to insert data and execute
        sql_query = """ INSERT INTO chatbots (
            bot_name,
            username,
            password
        ) VALUES (?,?,?)"""
        query_data = (bot_name, username, password,)
        
        try:
            self.cursor.execute(sql_query, query_data)
            self.conn.commit()
        except sqlite3.Error as err:
            # Display an error message and exit
            print("[E] Error creating chatbot: {}".format(err))
            exit(1)
            
    def modify(self, bot_name, username, password):
        """ Modify a bot
        
        Arguments:
            bot_name - string - The name of the bot
            username - string - The Kik username
            password - string - The Kik password
        """
        
        # Create the query
        sql_query = """ UPDATE chatbots SET 
            bot_name=?,
            username=?,
            password=? WHERE id=?; """
        query_data = (bot_name, username, password)
        
        # Attempt to run the query
        try:
            self.cursor.execute(sql_query, query_data)
            self.conn.commit()
        except sqlite3.Error as err:
            print("[E] Error modifying bot: {}".format(err))
            exit(1)
            
    def delete(self, bot_name):
        """ Delete a bot
        
        Arguments:
            bot_name - string - The bot to delete
        """
        
        # Create the query
        sql_query = """ DELETE FROM chatbots WHERE bot_name=?; """
        query_data = (bot_name,)
        
        # Attempt to run the query
        try:
            self.cursor.execute(sql_query, query_data)
            self.conn.commit()
        except sqlite3.Error as err:
            print("[E] Error deleting bot: {}".format(err))
            exit(1)
            
    def info(self, bot_name):
        """ Get a bots database entry
        
        Arguments:
            bot_name - string - The bot to get info on
        """
        
        # Create and run the query
        sql_query = """ SELECT * FROM chatbots WHERE bot_name=? """
        query_data = (bot_name,)
        self.cursor.execute(sql_query, query_data)
        bot_info = self.cursor.fetchone()
        
        # Return the info
        return bot_info