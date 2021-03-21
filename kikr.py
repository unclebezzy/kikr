#!/usr/bin/python3

"""
Kikr Kik Chatbot Spawner
Version 0.1
By Uncle Bezzy and Killida1
"""

# Imports
import os
import sys
import getopt
import sqlite3
import threading

def main(argv):
    """ Process command line argument and act as parent threading
    
    Arguments:
        argv - list - The command line arguments passed
    """
    
    # Attempt to process arguments
    try:
        opts, args = getopt.getopt(argv, "hv", ("help", "version"))
    except getopt.GetoptError as err:
        print("[E] Error processing arguments: {}!".format(err))
        exit(1)
        
    # Set default values
    action = None
    bot_name = None
    bot_name_list = None
    
    # Process arguments one-by-one
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # Display the help message and exit
            print("USAGE:")
            print("\tkikr [-h] [-v] [-l] [-nmd BOT_NAME] [-s BOT_NAME_LIST]")
            print("")
            print("Python based Kik bot creation software")
            print("")
            print("ARGUMENTS:")
            print("\t-h, --help\tDisplay the help message")
            print("\t-v, --version\tDisplay the version message")
            print("\t-l, --list\tList all bots")
            print("\t-n, --new BOT_NAME\tCreate a new bot")
            print("\t-m, --modify BOT_NAME\tModify a bot")
            print("\t-d, --delete BOT_NAME\tDelete a bot")
            print("\t-s, --start BOT_NAME_LIST\tA comma seperated list of bots to start")
            exit(0)
            
        elif opt in ("-v", "--version"):
            # Display the version message and exit
            print("Kikr Kik Bot Spawner")
            print("Version 0.1")
            print("By Uncle Bezzy and Killida1")
            exit(0)
            
        elif opt in ("-l", "--list"):
            # List all chatbots
            action = "list"
            
        elif opt in ("-n", "--new"):
            # Create a new bot
            action = "new"
            bot_name = arg
            
        elif opt in ("-m", "--modify"):
            # Modify a bot
            action = "modify"
            bot_name = arg
            
        elif opt in ("-d", "--delete"):
            # Delete a bot
            action = "delete"
            bot_name = arg
            
        elif opt in ("-s", "--start"):
            # Start bots
            action = "start"
            bot_name_list = args
            
    # Display intro message
    print("#####Kikr v0.1#####")
    print("[I] Initializing...")
    print("[***] ...Connecting to database")
            
    # Connect to the SQLite database
    db_file = "rsc/kikr.db"
    db_manager = DatabaseManager(db_file)
    
    # Display status message
    print("[***]...Connected to database")
    
    # Process actions
    if action == "list":
        # List all chatbots
        bot_list = db_manager.list()
        print(bot_list)
        
    elif action == "new":
        # Create a new chatbot
        # Print status message
        print("[I] Creating new bot...")
        
        # Get the username and password
        username = input("[***] >Username: ")
        password = input("[***] >Password: ")
        
        # Print status message
        print("[***] ...Adding bot to database")
        
        # Add the new bot to the database
        db_manager.new(bot_name, username, password)
        
        # Print status message
        print("[***...Bot added to database")
        
    elif action == "modify":
        # Modify a bot
        # Print status message
        print("[I] Modifying bot {}".format(bot_name))
        
        # Get the new information
        bot_name = input("[***] >Bot Name: ")
        username = input("[***] >Username: ")
        password = input("[***] >Password: ")
        
        # Print status message
        print("[***] ...Updating entry in database")
        
        # Update the bots database entry
        db_manager.modify(bot_name, username, password)
        
        # Print status message
        print("[***] ...Entry updated")
        
    
    elif action == "delete":
        # Delete a bot
        # Print status message
        do_it = input("[I] >Delete bot {}? (y/n): ")
        
        if do_it == "y":
            # Print status message and delete bot
            print("[***] ...Deleting bot")
            db_manager.delete(bot_name)
            print("[***] ...Bot deleted")
            
        else:
            print("[***] Aborting...")
            exit(0)
            
    elif action == "start":
        # Start the bots
        for bot in bot_name_list:
            ThreadManager.start(bot)

# Run the script
if __name__ == "__main__":
    main(sys.argv[1:])