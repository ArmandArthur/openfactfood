#! /usr/bin/env python3
# coding: utf-8

import mysql.connector

class Database:
    # Instance.
    __instance = None

    # Connexion BDD
    database_host = "127.0.0.1"
    database_user = "root"
    #database_passwd = "arthur"
    database_passwd = "rootAdmin!!"
    database_name = "openfoodfacts" 
    database_file = "database_structure.sql"

    @staticmethod
    def getInstance():
        #Instance if not exist
        if Database.__instance == None:
            Database()
        return Database.__instance

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=self.database_host,
            user=self.database_user,
            passwd=self.database_passwd,        
        )
        
        self.database = mysql.connector.connect(
            host=self.database_host,
            user=self.database_user,
            passwd=self.database_passwd,
            database=self.database_name           
        )

        if Database.__instance != None:
            raise Exception("La classe est un singleton.")
        else:
            Database.__instance = self