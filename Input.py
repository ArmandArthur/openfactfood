#! /usr/bin/env python3
# coding: utf-8

#from Database import Database
from Color import Color
from RequestCategory import RequestCategory
from RequestProduct import RequestProduct
from RequestSubstitu import RequestSubstitu
from colorama import init

class Input:

    """
        Récupère les "modeles" requetes
        [EN] - GET request model
    """
    def __init__(self):
        init()
        self.requestCategoryInstance = RequestCategory()
        self.requestProductInstance = RequestProduct()
        self.requestSubstituInstance = RequestSubstitu()
        self.display_menu()

    """
        Selection du type de menu, si choix non conforme, rappel de la fonction
        [EN] - Choice of the menu, if choice fails, call the function itself
    """
    def display_menu(self):
        print("\n")
        print(Color.WARNING + " 1 - Quel aliment souhaitez-vous remplacer ? " + Color.ENDC)
        print(Color.WARNING + " 2 - Retrouver mes aliments substitues " + Color.ENDC)
        print("\n")
        print(Color.HEADER)
        choice_menu = input("Faites votre choix")
        try:
            choice_menu = int(choice_menu)
        except ValueError:
            self.display_menu()
        

        if choice_menu == 1 :
            self.categorie_menu()
        # Retrouver mes substitus
        elif choice_menu == 2 :
            self.substitu_menu()

    """
        Liste la liste des catégories
        Affiche le nombre de résultats de la requetes.
        [EN] - List the categories
        [EN] - Display the count of categories
    """
    def categorie_menu(self):
        # pour avoir les attributs au lieu des tuples
        parameters =  self.requestCategoryInstance.liste()
        print("\n")
        print(Color.OKGREEN + "Le programme a retourné {} catégorie".format(parameters['cursor'].rowcount)+ Color.ENDC)
        print("\n")
        self.categorie_print(parameters['categories'])
        self.categorie_input()

    """
        Affiche les catégories
        [EN] - Display categories
    """
    def categorie_print(self, categories):
        for categorie in categories:
            print (Color.WARNING + "{} -- {}".format(categorie.id, categorie.name)+ Color.ENDC)
        print("\n")
    
    """
        Propose à l'utilisateur de sélectionner l'id du catégorie
        Si ID non conforme, rappel de la function categorie_menu
        Idem, si ID conforrme mais pas de résultats sur la catégorie.
        Sinon, affichage de la liste des produits avec le choix de la catégorie
        
        [EN] - User's choice to choose ID's category
        [EN] - If ID not integer, call categorie_menu function
        [EN] - If ID is integer but no categorie found, call categorie_menu function
        [EN] - Else, display list of product with the choice_categorie
    """
    def categorie_input(self):
        print(Color.HEADER)
        choice_categorie = input("Selectionner l'id d'une categorie : ")
        try:
            choice_categorie = int(choice_categorie)
            self.categorie_exist(choice_categorie)
        except ValueError:
            self.categorie_menu()        
        
    """
        Expliqué dans le docstring de la fonction categorie_input
        
        [EN] - Explain in the doctring of the function categorie_input
    """
    def categorie_exist(self, choice_categorie):
        parameters = self.requestCategoryInstance.exist(choice_categorie)
        if not parameters['rows']:
            # Si pas de categorie trouvée, on affiche le menu de base
            self.categorie_menu()
        else:
            # Si une catégorie est trouvée, on affiche le menu des produits avec comme
            # paramètre le choix de la catégorie
            self.produit_menu(choice_categorie)
    """
        Le programme écrit le nombre de produits retournés par la requetes
        Appel de la fonction produit_print et produit_input
        
        [EN] - Computer write the count of products found.
        [EN] - Call function produit_print and produit_input
        
    """
    def produit_menu(self, choice_categorie):
        parameters = self.requestProductInstance.liste_from_category(choice_categorie)
        print("\n")
        print(Color.OKGREEN + "Le programme a retourné {} produits".format(parameters['cursor'].rowcount)+ Color.ENDC)
        print("\n")
        self.produit_print(parameters['produits'])
        self.produit_input(choice_categorie)

    """
        Affichage de la liste des produits avec espacements réguliers
        
        [EN] - Display the list of product's attributes with regular alignment.
        
    """
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

    """
        Sélection de l'ID du produit, vérification si le produit existe
        
        [EN] - Chooce of ID's product, verify si product exist
    """
    def produit_input(self, choice_categorie):
        print(Color.HEADER)
        choice_produit = input("Selectionner l'id d'un produit : ")
        try:
            choice_produit = int(choice_produit)
            self.produit_exist(choice_produit, choice_categorie)        
        except ValueError:
            self.produit_menu(choice_categorie)        

    """
        Vérification si le produit existe dans la catégorie
        Si pas résultats, le produit n'appartient pas à la catégorie, retour à la liste des produits de la catégorie
        Sinon recherche d'un substitu

        [EN] - Verify in the product exist in the category
        [EN] - If no results, product don't behove of the category, back to the list of product of category
        [EN] - Else search a subsitute
    """
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

    """
        produit_find retourne un produit correspondant à l'ID du produit
        letter_before retourne un tableau avec les nutriscores supérieurs à celui du produit
        substitu_find retourne un produit de subsitu trouvé
        Si résultats, affichage du produit substitu trouvé, et appel à la proposition de sauvegarde.
        Sinon, on recherche la catégorie du produit sélectionné pour afficher la liste des produits correspondants
        à cette catégorie.

        [EN] - produit_find return a product corresponding to the ID product
        [EN] - letter_before return an array with nutriscores better than nutriscore of product choosen.
        [EN] - substitu_find return a product substitute
        [EN] - If results, display product substitute found, and call question of save.
        [EN] - Else, find the category of product choose for for displaying the liste of products corresponding 
        to this category.

    """
    def produit_substitu_search(self, choice_produit):

        produit_item = self.produit_find(choice_produit)   
        nutriscore_liste = self.letter_before(produit_item.nutriscore)
        produit_substitu = self.substitu_find(choice_produit, nutriscore_liste)
        if produit_substitu is not None:
            self.produit_item_print(produit_substitu)
            self.produit_substitu_input(produit_item, produit_substitu)
        else:
            print("\n")
            print("Aucun produit substitu de trouver...")
            # Recherche de la catégorie du produit pour lancer le menu des produits
            parameters = self.category_find(choice_produit)
            self.produit_menu(parameters['categorie'].id)

    """ GET the category from product_id  """
    def category_find(self, choice_produit):
        parameters = self.requestProductInstance.category_find(choice_produit)
        return parameters

    """ 
        Voulez vous sauvegarder le substitu en base?
        produit_substitu_save fait un insert ou un update.
        Si enregistré, message de confirmation + appel du menu principal
        Si choix non, appel du menu principal
        Sinon, si l'utilisateur n'a pas choici oui ou non, on rappel la fonction
    
        [EN] - Do you want save the subsitute in database?
        [EN] - If saved, confirmation message and call menu first
        [EN] - If chooce no, call menu first
        [EN] - Else, recall the same function
    """

    def produit_substitu_input(self, produit_item, produit_substitu):
        print(Color.HEADER)
        choice_save = input("Voulez vous enregistrer en base de données le substitu? (oui/non) ")
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

    """ 
        Retourne true or false si le produit subsitu existe déjà

        [EN] - Return true or false if the product exist or not.
    """
    def produit_substitu_exist(self, produit_item):
        isExist = self.requestSubstituInstance.exist(produit_item)
        return isExist

    """ 
        Retourne true si le produit est insérer/updater (pour le message)
        [EN] - Return true if product subsitute is insert/update (for the message).

    """
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

    """ 
        Recherche un produit par son ID - appelé par produit_substitu_search
        [EN] - Search a product by a ID - call by produit_substitu_search

    """
    def produit_find(self, choice_produit):
        parameters = self.requestProductInstance.find(choice_produit)
        return parameters['produit']

    """ 
        Recherche un produit substitu par le nutriscore et la catégorie du produit
         - appelé par produit_substitu_search
        [EN] - Search a product substitute by nutriscore and product's category
         - call by produit_substitu_search

    """
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

    """ 
        Construit le WHERE_IN de la requete
         - appelé par produit_substitu_search
        [EN] - Build WHERE_IN of request
         - call by produit_substitu_search

    """
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

    """ 
        Liste des substituts trouvés
        Appelle la fonction print et l'input

        [EN] - List of substitutes found
        [EN] - Call function print and input
        
    """    
    def substitu_menu(self):
        parameters = self.requestSubstituInstance.liste()
        print("\n")
        print(Color.OKGREEN + "Le programme a retourné {} produits qui ont un subsititu ".format(parameters['cursor'].rowcount)+ Color.ENDC)
        print("\n")
        self.produit_print(parameters['products'])
        self.substitu_input()

    """ 
        Choix du produit sur lequel on veut avoir le substitut

        [EN] - Choose product where we want see the substitute
        
    """    
    def substitu_input(self):
        print(Color.HEADER)
        choice_product = input("Selectionner l'id d'un produit : ")
        try:
            choice_product = int(choice_product)
            isExist = self.substitu_exist(choice_product)
            if isExist == True:
                self.substitu_item(choice_product)
            else:
                self.substitu_menu()
        except ValueError:
            self.substitu_menu()   

    """ 
        Vérifie si un substitu existe

        [EN] - Vérify if a substitue exist
        
    """    
    def substitu_exist(self, choice_product):
        parameters = self.requestProductInstance.find(choice_product)
        isExist = self.requestSubstituInstance.exist(parameters['produit'])
        return isExist

    """ 
        Affiche le subsitue puis le menu principal

        [EN] - Display the substitute and call the main menu
        
    """    
    def substitu_item(self, choice_product):
        parameters = self.requestSubstituInstance.item_from_product(choice_product)
        self.produit_item_print(parameters['product'])
        self.display_menu()