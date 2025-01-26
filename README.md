# Project_Geomatics

Showcasing the monuments of France in a map with the possibilty to filter by region and department, and see the image of each monument,

Original map  is https://data.culture.gouv.fr/explore/dataset/liste-des-immeubles-proteges-au-titre-des-monuments-historiques/export/?disjunctive.departement_en_lettres&location=8,16.82032,-61.57837

The map we use is a filtered version of the original map to reduce the size of the file from 200 MB 35.3 MB using "filter" in QGIS then exporting the map
We filtered by 
- reference
- historique
-  "adresse_forme_editoriale" not used but to have less rows
- domaine
- titre éditorial de la notice
- commune forme éditoriale
- departement_format_numerique
- format abrege_de_siecle_de_construction
Now we have 6916 features instead of 40000 which speeds up the loading and manipulation of the map