
CREATE TABLE marques (
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
);


CREATE TABLE categories (
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
);


CREATE TABLE produits (
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                marque_id INT NOT NULL,
                nutriscore VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
);


CREATE TABLE favoris (
                produit_id INT NOT NULL,
                produit_substitu_id INT NOT NULL,
                PRIMARY KEY (produit_id, produit_substitu_id)
);


CREATE TABLE asso_produit_categorie (
                categorie_id INT NOT NULL,
                produit_id INT NOT NULL,
                PRIMARY KEY (categorie_id, produit_id)
);


ALTER TABLE produits ADD CONSTRAINT marques_produits_fk
FOREIGN KEY (marque_id)
REFERENCES marques (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE asso_produit_categorie ADD CONSTRAINT categories_asso_produit_categorie_fk
FOREIGN KEY (categorie_id)
REFERENCES categories (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE asso_produit_categorie ADD CONSTRAINT produits_asso_produit_categorie_fk
FOREIGN KEY (produit_id)
REFERENCES produits (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE favoris ADD CONSTRAINT produits_favoris_fk
FOREIGN KEY (produit_id)
REFERENCES produits (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE favoris ADD CONSTRAINT produits_favoris_fk1
FOREIGN KEY (produit_substitu_id)
REFERENCES produits (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
