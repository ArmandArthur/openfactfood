#! /usr/bin/env python3
# coding: utf-8

import requests
import mysql.connector

class Main:

    url = "https://fr.openfoodfacts.org"
    database_host = "locahost"
    database_user = "root"
    database_passwd = ""
    database_name = "openfoodfacts" 
    database_file = "database_structure.sql"

    def __init__(self):
        #self.database_create()
        #self.database_build()
        self.database_set_values()


    def database_create(self):
        self.database = mysql.connector.connect(
            host=self.database_host,
            user=self.database_user,
            passwd=self.database_passwd
           
        )
        cursor = self.database.cursor()

        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format("openfoodfacts"))

        
    def database_build(self):
        self.database = mysql.connector.connect(
            host=self.database_host,
            user=self.database_user,
            passwd=self.database_passwd,
            database=self.database_name
           
        )
        cursor = self.database.cursor()

        fd = open(self.database_file, 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')

        for command in sqlCommands:
            try:
                if command.strip() != '':
                    cursor.execute(command)
            except IOError :
                print(msg)

Main()