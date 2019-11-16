#! /usr/bin/env python3
# coding: utf-8
"""
    Import
"""
from Database import Database

class RequestProduct:
    """
        Request about product
    """
    def __init__(self):
        """
            Init
        """
        self.database = Database.updateInstance().database
     
    def liste_from_category(self, choice_categorie):
        """
            List product by category
        """
        cursor = self.database.cursor(named_tuple=True, buffered=True)
        sql = ("SELECT produits.* "\
               "FROM asso_produit_categorie "\
               "INNER JOIN produits ON produits.id = asso_produit_categorie.produit_id "\
               "WHERE asso_produit_categorie.categorie_id = {} ".format(choice_categorie))
        cursor.execute(sql)
        produits = cursor.fetchall()

        parameters = {}
        parameters['cursor'] = cursor
        parameters['produits'] = produits

        return parameters

    def exist(self, choice_produit, choice_categorie):
        """
            Verify if the product exist in categorie
        """
        cursor = self.database.cursor(buffered=True)
        sql = ("SELECT * "\
               "FROM produits "\
               "INNER JOIN asso_produit_categorie "\
               "ON produits.id = asso_produit_categorie.produit_id "\
               "WHERE produits.id = '{}' AND asso_produit_categorie.categorie_id = '{}' "
               .format(choice_produit, choice_categorie))
        cursor.execute(sql)
        rows = cursor.fetchall()

        parameters = {}
        parameters['rows'] = rows

        return parameters

    def find(self, choice_produit):
        """
            Find a product
        """
        cursor = self.database.cursor(named_tuple=True, buffered=True)
        sql = "SELECT produits.* FROM produits WHERE produits.id =  '{}' ".format(choice_produit)
        cursor.execute(sql)
        produit = cursor.fetchone()

        parameters = {}
        parameters['produit'] = produit

        return parameters

    def category_find(self, choice_produit):
        """
            Find the category of product
        """
        cursor = self.database.cursor(named_tuple=True, buffered=True)
        sql = ("SELECT categories.* "
               "FROM categories "\
               "INNER JOIN asso_produit_categorie "\
               "ON categories.id = asso_produit_categorie.categorie_id "\
               "INNER JOIN produits ON  produits.id = asso_produit_categorie.produit_id "\
               "WHERE produits.id =  '{}' ".format(choice_produit))
        cursor.execute(sql)
        categorie = cursor.fetchone()

        parameters = {}
        parameters['categorie'] = categorie

        return parameters
        