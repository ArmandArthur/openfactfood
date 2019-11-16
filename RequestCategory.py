#! /usr/bin/env python3
# coding: utf-8
"""
    Import
"""
from Database import Database

class RequestCategory:
    """
        Request about category
    """

    def __init__(self):
        """
            Init
        """
        self.database = Database.updateInstance().database

    def liste(self):
        """
            List of categories
        """
        cursor = self.database.cursor(named_tuple=True)
        sql = "SELECT * FROM categories"
        cursor.execute(sql)
        categories = cursor.fetchall()

        parameters = {}
        parameters['cursor'] = cursor
        parameters['categories'] = categories

        return parameters

    def exist(self, choice_categorie):
        """
           Verify is the categoy is present in database
        """
        cursor = self.database.cursor()
        sql = "SELECT * FROM categories WHERE id = '{}' ".format(choice_categorie)
        cursor.execute(sql)
        rows = cursor.fetchall()

        parameters = {}
        parameters['rows'] = rows

        return parameters
