#! /usr/bin/env python3
# coding: utf-8

from Database import Database

class RequestCategory:

    def __init__(self):
        self.database = Database.updateInstance().database
        
    def liste(self):
        cursor = self.database.cursor(named_tuple=True)
        sql = "SELECT * FROM categories"
        cursor.execute(sql)
        categories = cursor.fetchall()

        parameters = {}
        parameters['cursor'] = cursor
        parameters['categories'] = categories

        return parameters

    def exist(self, choice_categorie):
        cursor = self.database.cursor()
        sql = "SELECT * FROM categories WHERE id = '{}' ".format(choice_categorie)
        cursor.execute(sql)
        rows = cursor.fetchall()

        parameters = {}
        parameters['rows'] = rows

        return parameters