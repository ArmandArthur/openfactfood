#! /usr/bin/env python3
# coding: utf-8

import requests
import mysql.connector

class Main:

    url = "https://fr.openfoodfacts.org"
    database_host = "127.0.0.1"
    database_user = "root"
    database_passwd = "arthur"
    database_name = "openfoodfacts" 
    database_file = "database_structure.sql"

    url_liste = []

    def __init__(self):
        #self.database_create()
        #self.database_build()
        self.database_set_values()


    def database_set_values(self):
        self.url_yaourt_caramel = self.url+"/categorie/yaourts-au-caramel.json"
        self.url_cremes_dessert_cafe  = self.url+"/categorie/cremes-dessert-cafe.json" 

        self.url_liste.append(self.url_yaourt_caramel)
        self.url_liste.append(self.url_cremes_dessert_cafe)

        self.database = mysql.connector.connect(
            host=self.database_host,
            user=self.database_user,
            passwd=self.database_passwd,
            database=self.database_name
           
        )

        for i in self.url_liste:
            request = requests.get(i)
            categorie = request.json()

            # Save a categorie
            cursor = self.database.cursor()
            sql = "INSERT INTO categories (name) VALUES (%s) "
            cursor.execute(sql, (i,) ) # sans la virgule, il y a un bug.
            self.database.commit()
            categorie_id = cursor.lastrowid

            #Save a brand
            for j, product in enumerate(categorie['products']):
                cursor = self.database.cursor()
                brand_label = product['brands']
                sql = "SELECT * FROM marques WHERE name = '"+brand_label+"' "
                rs = cursor.execute(sql)
                rows = cursor.fetchall()
                if not rows:
                    cursor = self.database.cursor()
                    sql = "INSERT INTO marques (name) VALUES (%s) "
                    cursor.execute(sql, (brand_label,) ) # sans la virgule, il y a un bug.
                    self.database.commit()
                    brand_id = cursor.lastrowid
                else:  
                    brand_id = rows[0][0]
                            
                #Save the product
                cursor = self.database.cursor()
                sql = "INSERT INTO produits (name, marque_id, nutriscore, url) VALUES (%s,%s,%s,%s)"
                product_name = product['product_name']
                product_nutriscore = product['nutrition_grades_tags'][0]
                product_url = product['url']
                cursor.execute(sql, (product_name, brand_id, product_nutriscore, product_url,) ) # sans la virgule, il y a un bug.
                self.database.commit()
                product_id = cursor.lastrowid

                #Save the association after insert product and categorie
                cursor = self.database.cursor()
                sql = "INSERT INTO asso_produit_categorie (categorie_id, produit_id) VALUES (%s,%s)"
                cursor.execute(sql, (categorie_id, product_id,) )
                self.database.commit()


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

        f_open = open(self.database_file, 'r')
        sql_file = f_open.read()
        f_open.close()

        sql_commandes = sql_file.split(';')

        for command in sql_commandes:
            try:
                if command.strip() != '':
                    cursor.execute(command)
            except IOError :
                print(msg)

Main()