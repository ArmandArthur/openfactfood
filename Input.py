#! /usr/bin/env python3
# coding: utf-8

#from Database import Database
from Color import Color
from RequestCategory import RequestCategory
from RequestProduct import RequestProduct
from RequestSubstitu import RequestSubstitu

class Input:

    def __init__(self):
        self.requestCategoryInstance = RequestCategory()
        self.requestProductInstance = RequestProduct()
        self.requestSubstituInstance = RequestSubstitu()
        self.display_menu()

    def display_menu(self):
        print("\n")
        print(Color.WARNING + " 1 - Quel aliment souhaitez-vous remplacer ? " + Color.ENDC)
        print(Color.WARNING + " 2 - Retrouver mes aliments substitues " + Color.ENDC)
        print("\n")
        choice_menu = input(Color.HEADER + "Faites votre choix : " + Color.ENDC)
        try:
            choice_menu = int(choice_menu)
        except ValueError:
            self.display_menu()
        

        if choice_menu == 1 :
            self.categorie_menu()
        # Retrouver mes substitus
        elif choice_menu == 2 :
            print('ko')

    def categorie_menu(self):
        # pour avoir les attributs au lieu des tuples
        parameters =  self.requestCategoryInstance.liste()
        print("\n")
        print(Color.OKGREEN + "Le programme a retourné {} catégorie".format(parameters['cursor'].rowcount)+ Color.ENDC)
        print("\n")
        self.categorie_print(parameters['categories'])
        self.categorie_input()

    def categorie_print(self, categories):
        for categorie in categories:
            print (Color.WARNING + "{} -- {}".format(categorie.id, categorie.name)+ Color.ENDC)
        print("\n")
    
    def categorie_input(self):
        choice_categorie = input(Color.HEADER + "Selectionner l'id d'une categorie : "+ Color.ENDC)
        try:
            choice_categorie = int(choice_categorie)
            self.categorie_exist(choice_categorie)
        except ValueError:
            self.categorie_menu()        
        

    def categorie_exist(self, choice_categorie):
        parameters = self.requestCategoryInstance.exist(choice_categorie)
        if not parameters['rows']:
            # Si pas de categorie trouvée, on affiche le menu de base
            self.categorie_menu()
        else:
            # Si une catégorie est trouvée, on affiche le menu des produits avec comme
            # paramètre le choix de la catégorie
            self.produit_menu(choice_categorie)

    def produit_menu(self, choice_categorie):
        parameters = self.requestProductInstance.liste_from_category(choice_categorie)
        print("\n")
        print(Color.OKGREEN + "Le programme a retourné {} produits".format(parameters['cursor'].rowcount)+ Color.ENDC)
        print("\n")
        self.produit_print(parameters['produits'])
        self.produit_input(choice_categorie)

    def produit_print(self, produits):
        for produit in produits:
            print (Color.WARNING + "{:<3} -- {:<70} -- {:<2} ".format(produit.id, produit.name, produit.nutriscore) + Color.ENDC)
        print("\n")

    def produit_item_print(self, produit):
            print("\n")
            print (Color.OKGREEN + "Le programme a retourné 1 substitu: "+ Color.ENDC)
            print("\n")
            print (Color.WARNING + "{} -- {} -- {} ".format(produit.id, produit.name, produit.nutriscore)+ Color.ENDC)
            print("\n")

    def produit_input(self, choice_categorie):
        choice_produit = input(Color.HEADER + "Selectionner l'id d'un produit : " + Color.ENDC)
        try:
            choice_produit = int(choice_produit)
            self.produit_exist(choice_produit, choice_categorie)        
        except ValueError:
            self.produit_menu(choice_categorie)        


    def produit_exist(self, choice_produit, choice_categorie):
        parameters = self.requestProductInstance.exist(choice_produit, choice_categorie)
        if not parameters['rows']:
            # Si pas de produit trouvé, on affiche le menu des produits
            print("\n")
            print(Color.OKGREEN + "Le produit saisi n'appartient pas à la catégorie saisie" + Color.ENDC)
            self.produit_menu(choice_categorie)
        else:
            # Si une produit est trouvé, on affiche le menu du substitu
            self.produit_substitu_search(choice_produit)

    def produit_substitu_search(self, choice_produit):

        produit_item = self.produit_find(choice_produit)   
        nutriscore_liste = self.letter_before(produit_item.nutriscore)
        produit_substitu = self.substitu_find(choice_produit, nutriscore_liste)
        if produit_substitu is not None:
            self.produit_item_print(produit_substitu)
            self.produit_substitu_input(produit_item, produit_substitu)
        else:
            print("Aucun produit substitu de trouver...")
            # Recherche de la catégorie du produit pour lancer le menu des produits
            categorie = self.category_find(choice_produit)
            self.produit_menu(categorie.id)

    """ GET the category from product_id  """
    def category_find(self, choice_produit):
        parameters = self.requestProductInstance.category_find(choice_produit)
        return parameters

    def produit_substitu_input(self, produit_item, produit_substitu):
        choice_save = input(Color.HEADER + "Voulez vous enregistrer en base de données le substitu? (oui/non) " + Color.ENDC)
        if choice_save == 'oui':
            isInsert = self.produit_substitu_save(produit_item, produit_substitu)
            if isInsert == True :
                print("\n")
                print (Color.OKGREEN + "Le programme a enregistré le substitu du produit {} ".format(produit_item.name)+ Color.ENDC)
            self.display_menu()
            
        elif choice_save == 'non': 
            self.display_menu()
        else :
            self.produit_substitu_input(produit_item, produit_substitu)

    def produit_substitu_exist(self, produit_item):
        isExist = self.requestSubstituInstance.exist(produit_item)
        return isExist

    def produit_substitu_save(self, produit_item, produit_substitu):
        is_produit_substitu_exist = self.produit_substitu_exist(produit_item)
        if is_produit_substitu_exist == True :
            isAction = self.produit_substitu_update(produit_item, produit_substitu)
        else :
            isAction = self.produit_substitu_insert(produit_item, produit_substitu)

        return isAction 

    def produit_substitu_insert(self, produit_item, produit_substitu):
        parameters = self.requestSubstituInstance.insert(produit_item, produit_substitu)
        if parameters['cursor'].rowcount is not None:
            return True
        else:
            return False

    def produit_substitu_update(self, produit_item, produit_substitu):
        parameters = self.requestSubstituInstance.update(produit_item, produit_substitu)
        if parameters['cursor'].rowcount is not None:
            return True
        else:
            return False

    def produit_find(self, choice_produit):
        parameters = self.requestProductInstance.find(choice_produit)
        return parameters['produit']

    def substitu_find(self, choice_produit, nutriscore_liste):
        # Recherche de la catégorie du produit
        parameters = self.category_find(choice_produit)

        # Construction du IN
        nutriscore_in = "("
        for item in nutriscore_liste:
            nutriscore_in += " '"+item+"', "
        nutriscore_in = nutriscore_in[:-2]
        nutriscore_in += ")"

        # Recherche d'un substitu
        params = self.requestSubstituInstance.find(parameters['categorie'], nutriscore_in)
        return params['product_substitu']


    def letter_before(self, nutriscore):
        alphabetic = "abcdefghijklmnopqrstuvwxyz"
        position = alphabetic.find(nutriscore)
        if position != 1:
            nutriscore_better = alphabetic[position]        
        else:
            nutriscore_better = alphabetic[0]

        liste_literal = []
        if nutriscore_better == 'a' :
            liste_literal.append(nutriscore_better)
        else :
            nutriscore_liste = alphabetic.split(nutriscore_better)[0]
            for item in nutriscore_liste:
                liste_literal.append(item)

        return liste_literal
        
