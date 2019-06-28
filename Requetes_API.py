#-*- coding: utf-8 -*-

# url catÃ©gories : https://fr.openfoodfacts.org/categories.json
#{
#name: "Aliments et boissons Ã  base de vÃ©gÃ©taux",
#id: "en:plant-based-foods-and-beverages",
#url: "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux",
#products: 28110
#},
# url produit : https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux/1.json
# Ensuite 20 produits par page

from math import ceil
import requests
#import json #pour affichage
LIMITE = 5
url_de_base = "https://fr.openfoodfacts.org/categorie/" # on rajoute produit/i.json
print(" . . . Veuillez patienter... Requete en cours. . . ")
r = requests.get('https://fr.openfoodfacts.org/categories.json')
categories = r.json()
nombre_categories = categories["count"]
print(" {} catégories présentes sur le site.".format(nombre_categories))
#Environs 12 800 catÃ©gories. Je vais commencer par en prendre une dizaine.
nombre_a_afficher = int(input("Combien de catÃ©gories voulez vous charger ? "))
# Je commence par nombre de produit par catï¿½gorie
nb_produit = LIMITE
total_produit = 0
total_charge = 0
for i in range(nombre_a_afficher):
    print("\n##############################")
    print(i+1," - ", end = " ")
    print(categories["tags"][i]["name"])
    print(categories["tags"][i]["id"])
    nombre_produits = int(categories["tags"][i]["products"])
    total_produit += nombre_produits
    nombre_pages = ceil(nombre_produits / 20)
    print("\t Nombre de produits :", nombre_produits, end = " ")
    print("\t Nombre de pages :", nombre_pages)
    adresse = categories["tags"][i]["url"]
    print("\t",adresse)
    # ICI REMPLIRE LA TABLE CATEGORIES
    # VOIR MPD POUR STRUCTURE DE LA TABLE CATEGORIE
    for page in range(2):
        adresse = categories["tags"][i]["url"] + "/" + str(page+1) + ".json"
        p = requests.get(adresse)
        produits = p.json()
        for k in range(20):
            print(produits["products"][k]["product_name"])
            total_charge += 1
        # structure d'une page produit
        # {
        #     page_size: 20,
        #     page: "1",
        #     count: 29335,
        #     products: [],
        #     skip: 0
        # }
        # SUR UN PRODUIT QUELLES SONT LES INFORMATIONS INTERESSANTES ?
        # EXEMPLE dans product on  garde :
        # image_ingredients_small_url: "https://static.openfoodfacts.org/images/products/322/247/255/9276/ingredients_fr.13.200.jpg"
        # product_name_fr: "Riz Basmati naturellement parfumé Bio Casino"
        # image_url: "https://static.openfoodfacts.org/images/products/322/247/255/9276/front_fr.12.400.jpg"
        # nutrition_grades: "a"
        # nutrition_grades_tags: ["a"]
        # categories: "Aliments et boissons à base de végétaux,Aliments d'origine végétale,Aliments à base de fruits et de légumes,Conserves,Aliments à base de plantes en conserve,Desserts,Fruits et produits dérivés,Fruits en conserve,Fruits au sirop,Lychees au sirop"
        #categories_hierarchy: [
        # "en:plant-based-foods-and-beverages",
        # "en:plant-based-foods",
        # "en:cereals-and-potatoes",
        # "en:seeds",
        # "en:cereals-and-their-products",
        # "en:cereal-grains",
        # "en:rices",
        # "en:aromatic-rices",
        # "en:indica-rices",
        # "en:long-grain-rices",
        # "en:basmati-rices"
        # ],
        # stores: "Casino"

print("\n Ces {} catégories contiennent {} produits dont {} ont été chargés".format(nombre_a_afficher,total_produit,total_charge))
