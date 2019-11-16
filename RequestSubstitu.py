#! /usr/bin/env python3
# coding: utf-8
"""
    Import
"""
from Database import Database

class RequestSubstitu:
    """
        Request about substitu
    """
    def __init__(self):
        """
            Init
        """
        self.database = Database.updateInstance().database

    def find(self, category, nutriscore_in):
        """
            Search a product "substitu" by nutriscore better
        """
        cursor = self.database.cursor(named_tuple=True, buffered=True)
        sql = ("SELECT produits.* "\
               "FROM produits "\
               "INNER JOIN asso_produit_categorie "\
               "ON asso_produit_categorie.produit_id = produits.id "\
               "INNER JOIN categories "\
               "ON categories.id = asso_produit_categorie.categorie_id "\
               "WHERE categories.id =  '{}' "\
               "AND produits.nutriscore IN {} "\
               "ORDER BY produits.nutriscore ASC "\
               "LIMIT 1 ".format(category.id, nutriscore_in))
        cursor.execute(sql)
        product_substitu = cursor.fetchone()

        params = {}
        params['product_substitu'] = product_substitu
        return params

    def exist(self, product_item):
        """
            Verify if a product has a substitu
        """
        cursor = self.database.cursor(named_tuple=True, buffered=True)
        sql = "SELECT * FROM favoris WHERE produit_id = '{}' ".format(product_item.id)
        cursor.execute(sql)
        rows = cursor.fetchone()
        if not rows:
            return False
        return True

    def insert(self, product_item, product_substitu):
        """
            Insert subsitu product
        """
        cursor = self.database.cursor()
        sql = "INSERT INTO favoris (produit_id, produit_substitu_id) VALUES (%s,%s)"
        cursor.execute(sql, (product_item.id, product_substitu.id,))
        self.database.commit()

        params = {}
        params['cursor'] = cursor
        return params

    def update(self, product_item, product_substitu):
        """
            Update subsitu product
        """
        cursor = self.database.cursor()
        sql = " UPDATE favoris SET produit_substitu_id = %s WHERE produit_id = %s "
        cursor.execute(sql, (product_item.id, product_substitu.id,))
        self.database.commit()
        params = {}
        params['cursor'] = cursor
        return params

    def liste(self):
        """
            List of all substitu
        """
        cursor = self.database.cursor(named_tuple=True)
        sql = "SELECT * FROM produits INNER JOIN favoris ON favoris.produit_id = produits.id"
        cursor.execute(sql)
        products = cursor.fetchall()

        parameters = {}
        parameters['cursor'] = cursor
        parameters['products'] = products

        return parameters

    def item_from_product(self, choice_product):
        """
            Find the subsitu of one product
        """
        cursor = self.database.cursor(named_tuple=True)
        sql = ("SELECT produits.* "\
               "FROM favoris "\
               "INNER JOIN produits "\
               "ON produits.id = favoris.produit_substitu_id "\
               "AND favoris.produit_id = {} ".format(choice_product))
        cursor.execute(sql)
        product = cursor.fetchone()

        parameters = {}
        parameters['product'] = product
        return parameters
