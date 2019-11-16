#! /usr/bin/env python3
# coding: utf-8
"""
    import
"""
import requests
from Database import Database
from Config import *
import logging

class Setup:
    """
        Class SETUP
    """
    url = "https://fr.openfoodfacts.org"
    url_liste = []

    def __init__(self):
        self.connection = Database.getInstance().connection
        database_exist = self.database_exist()
        if database_exist is False:
            self.database_create()
            self.database = Database.updateInstance().database
            self.database_build()
        else:
            self.database = Database.updateInstance().database   
            self.database_set_values()

    def database_exist(self):
        """
            Verify if the database exist
        """
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT schema_name "+
            "FROM information_schema.schemata "+
            "WHERE schema_name = '"+database+"' ")
        rows = cursor.fetchall()
        if not rows:
            return False
        return True

    def database_set_values(self):
        """
            Request API and add results to local database
        """
        
        for url in categorie_liste:
            logging.warning(url)
            request = requests.get(categorie_base+url)
            categorie = request.json()

            # Save a categorie
            cursor = self.database.cursor()
            sql = "SELECT * FROM categories WHERE name = '"+url+"' "
            cursor.execute(sql)
            rows = cursor.fetchall()
            if not rows:
                cursor = self.database.cursor()
                sql = "INSERT INTO categories (name) VALUES (%s) "
                cursor.execute(sql, (url,)) # sans la virgule, il y a un bug.
                self.database.commit()
                categorie_id = cursor.lastrowid
            else:
                categorie_id = ""

            if categorie_id != '':
                #Save a brand
                for j, product in enumerate(categorie['products']):
                    #Save the product
                    cursor = self.database.cursor()
                    sql = ("INSERT INTO produits (name, marque_id, nutriscore, url)" +
                           " VALUES (%s,%s,%s,%s)")
                    product_name = product['product_name']
                    product_nutriscore = product['nutrition_grades_tags'][0]
                    product_url = product['url']
                    cursor.execute(sql, (product_name, 0, product_nutriscore, product_url,))
                    self.database.commit()
                    product_id = cursor.lastrowid

                    #Save the association after insert product and categorie
                    cursor = self.database.cursor()
                    sql = ("INSERT INTO asso_produit_categorie (categorie_id, produit_id)"+
                           " VALUES (%s,%s)")
                    cursor.execute(sql, (categorie_id, product_id,))
                    self.database.commit()

    def database_create(self):
        """
            Create database
        """
        cursor = self.connection.cursor()

        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))

    def database_build(self):
        """
            Read the requests and execute them
        """
        cursor = self.database.cursor()

        f_open = open('database_structure.sql', 'r')
        sql_file = f_open.read()
        f_open.close()

        sql_commandes = sql_file.split(';')

        for command in sql_commandes:
            try:
                if command.strip() != '':
                    cursor.execute(command)
            except IOError as err:
                print(err)
