#! /usr/bin/env python3
# coding: utf-8
"""
    import
"""
from collections import namedtuple
import mysql.connector
from Config import *

class Database:
    """
        Singleton
    """
    # Instance.
    __instance = None

    # Connexion BDD
    database_host = host
    database_user = user
    database_passwd = password
    database_name = database
    database_file = file_request

    @staticmethod
    def getInstance():
        """
            Create database
        """
        #Instance if not exist
        if Database.__instance is None:
            Database()
        return Database.__instance

    @staticmethod
    def updateInstance():
        """
            Updata connection database
        """
        if Database.__instance is None:
            Database()
        sub_attribute = namedtuple('database_function', 'database')
        Database.__instance = sub_attribute(mysql.connector.connect(
            host=Database.database_host,
            user=Database.database_user,
            passwd=Database.database_passwd,
            database=Database.database_name
        ))
        return Database.__instance

    def __init__(self):
        """
            Initialisation
        """
        self.connection = mysql.connector.connect(
            host=self.database_host,
            user=self.database_user,
            passwd=self.database_passwd,
        )
        if Database.__instance is not None:
            raise Exception("La classe est un singleton.")
        Database.__instance = self
