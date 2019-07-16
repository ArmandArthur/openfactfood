#! /usr/bin/env python3
# coding: utf-8

import requests
from Database import Database

class Setup:

    url = "https://fr.openfoodfacts.org"
    url_liste = []

    def __init__(self):
        self.connection = Database.getInstance().connection
        database_exist = self.database_exist()
        if database_exist == False :
            self.database_create()
            self.database = Database.updateInstance().database
            self.database_build()
            self.database_set_values()  


    def database_exist(self):
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT  schema_name FROM information_schema.schemata WHERE schema_name = 'openfoodfacts'")
        rows = cursor.fetchall()
        if not rows:
            return False
        else:
            return True

    def database_set_values(self):
        self.url_yaourt_caramel = self.url+"/categorie/yaourts-au-caramel.json"
        self.url_cremes_dessert_cafe  = self.url+"/categorie/cremes-dessert-cafe.json" 

        self.url_liste.append(self.url_yaourt_caramel)
        self.url_liste.append(self.url_cremes_dessert_cafe)

        for i in self.url_liste:
            request = requests.get(i)
            categorie = request.json()

            # Save a categorie
            cursor = self.database.cursor()
            sql = "SELECT * FROM categories WHERE name = '"+i+"' "
            rs_categorie = cursor.execute(sql)
            rows = cursor.fetchall()
            if not rows:
                cursor = self.database.cursor()
                sql = "INSERT INTO categories (name) VALUES (%s) "
                cursor.execute(sql, (i,) ) # sans la virgule, il y a un bug.
                self.database.commit()
                categorie_id = cursor.lastrowid
            #else:  
                #categorie_id = rows[0][0]

            if categorie_id != '':
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
        cursor = self.connection.cursor()

        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format("openfoodfacts"))

        
    def database_build(self):
        cursor = self.database.cursor()

        f_open = open('database_structure.sql', 'r')
        sql_file = f_open.read()
        f_open.close()

        sql_commandes = sql_file.split(';')

        for command in sql_commandes:
            try:
                if command.strip() != '':
                    cursor.execute(command)
            except IOError :
                print(msg)

