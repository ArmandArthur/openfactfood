#! /usr/bin/env python3
# coding: utf-8

from Database import Database

class Input:

    def __init__(self):
        self.database = Database.updateInstance().database
        self.display_menu()

    def display_menu(self):
        print(" 1 - Quel aliment souhaitez-vous remplacer ? ")
        print(" 2 - Retrouver mes aliments substitues ")
        choice_menu = input("Faites votre choix : ")
        choice_menu = int(choice_menu)

        if choice_menu == 1 :
            self.categorie_menu()
        # Retrouver mes substitus
        elif choice_menu == 2 :
        # Autrement, on relance la question primaire
            print('ko')
        else :
            self.display_menu()

    def categorie_menu(self):
        # pour avoir les attributs au lieu des tuples
        cursor = self.database.cursor(named_tuple=True)
        sql = "SELECT * FROM categories"
        cursor.execute(sql)
        categories = cursor.fetchall()

        self.categorie_print(categories)
        self.categorie_input()

    def categorie_print(self, categories):
        for categorie in categories:
            print ("{} -- {}".format(categorie.id,categorie.name))
    
    def categorie_input(self):
        choice_categorie = input("Selectionner l'id d'une categorie : ")
        choice_categorie = int(choice_categorie)
        self.categorie_exist(choice_categorie)

    def categorie_exist(self, choice_categorie):
        cursor = self.database.cursor()
        sql = "SELECT * FROM categories WHERE id = '{}' ".format(choice_categorie)
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            # Si pas de categorie trouvée, on affiche le menu de base
            self.categorie_input()
        else:
            # Si une catégorie est trouvée, on affiche le menu des produits avec comme
            # paramètre le choix de la catégorie
            self.produit_menu(choice_categorie)

    def produit_menu(self, choice_categorie):
        cursor = self.database.cursor(named_tuple=True)
        sql = "SELECT produits.* FROM asso_produit_categorie INNER JOIN produits ON produits.id = asso_produit_categorie.produit_id WHERE asso_produit_categorie.categorie_id = {} ".format(choice_categorie)
        cursor.execute(sql)
        produits = cursor.fetchall()

        self.produit_print(produits)
        self.produit_input(choice_categorie)

    def produit_print(self, produits):
        for produit in produits:
            print ("{} -- {} -- {} ".format(produit.id, produit.name, produit.nutriscore))

    def produit_input(self, choice_categorie):
        choice_produit = input("Selectionner l'id d'un produit : ")
        choice_produit = int(choice_produit)
        self.produit_exist(choice_produit, choice_categorie)

    def produit_exist(self, choice_produit, choice_categorie):
        cursor = self.database.cursor()
        # avec cette requete là, si on rentre 18, ça trouve un produit qui a une 
        # catégorie différente, ce qui est pas bon
        #sql = "SELECT * FROM produits WHERE id = '{}' ".format(choice_produit)
    def produit_exist(self, choice_produit, choice_categorie):
        cursor = self.database.cursor()
        sql = "SELECT * FROM produits INNER JOIN asso_produit_categorie ON produits.id = asso_produit_categorie.produit_id  WHERE produits.id = '{}' AND asso_produit_categorie.categorie_id = '{}' ".format(choice_produit, choice_categorie )
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            # Si pas de produit trouvé, on affiche le menu des produits
            self.produit_menu(choice_categorie)
        else:
            # Si une produit est trouvé, on affiche le menu du substitu
            print("else")
           