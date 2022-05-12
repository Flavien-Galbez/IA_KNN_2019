
"""
Created on Mon Apr 29 13:47:52 2019

@author: flavieng
"""

from math import sqrt
import csv
import numpy as np
from random import shuffle

fichier = open("iris.data", "r")
ligne = csv.reader(fichier)
coordonnees = list (ligne)

# Permet de decouper la base de donnee iris.data pour la mettre sous forme de tableau a 2 dimensions
for nbligne in range(len(coordonnees)-1):
  for nbcolonne in range (4):
    coordonnees[nbligne][nbcolonne] = float(coordonnees[nbligne][nbcolonne])
    
# Permet de calculer la distance entre 2 points du tableau    
def distance (coord1, coord2):
    resultat = 0
    for i in range (len (coord1)-1):
        resultat += (coord1 [i] - coord2 [i]) * (coord1 [i] - coord2 [i])
    return (sqrt (resultat))

# Permet de connaitre le voisin direct d'un point du tableau
def voisinProche1 (coord1):
    plusProche = 0
    minDist = -np.inf
    for i in range(len(coordonnees)-1): # On parcourt les donnees de tout le tableau
        dist = distance (coord1, coordonnees [i][0:4]) # on calcule la distance entre le point choisi et le reste du tableau
        if dist != 0 and dist < minDist:
            plusProche = i # Correspond au point le plus proche du point choisi
            minDist = dist 
    return (plusProche) # Retour le point qui est le plus proche

# Permet de connaitre les k voisins direct d'un point du tableau
def voisinProcheK1 (coord1, k):
  voisinage = []
  for i in range (len (coordonnees)-1): # On parcourt les donnees de tout le tableau
    voisinage.append (distance (coord1, coordonnees[i][0:4])) # On calcule toutes les distances entre le point choisi et le reste du tableau
  voisinTrouve = []
  for i in range (k):
    minDist = -np.inf
    for j in range (len (coordonnees)-1): # On parcourt les donnees de tout le tableau
      if voisinage [j] != 0 and voisinage [j] < minDist and j not in voisinTrouve: # Si la distance calcule est differente de 0 et inferieur a la plus petite distance et que cette valeur n'est pas deja dans les points selectionnes
        minDist = voisinage [j] # Alors mindist prend la distance entre le point choisi et le point verifie
        indice = j 
    voisinTrouve.append (indice) # Correspond aux points les plus proches du point choisi
  return (voisinTrouve) # Retour les points qui sont les plus proches

# Permet de connaitre le voisin direct d'un point du tableau d'une nouvelle base a partir de la base originale
def voisinProche2 (coord1):
    plusProche = 0
    minDist = -np.inf
    for i in range(len(nouvelleBDD)): # On parcourt les donnees de tout le tableau
        dist = distance (coord1, coordonnees [nouvelleBDD [i]][0:4]) # on calcule la distance entre le point choisi et le reste du tableau
        if dist != 0 and dist < minDist:
            plusProche = i # Correspond au point le plus proche du point choisi
            minDist = dist
    return (plusProche) # Retour le point qui est le plus proche

# Permet de connaitre les k voisins direct d'un point du tableau d'une nouvelle base a partir de la base originale
def voisinProcheK2 (coord1, k):
  voisinage = []
  for i in range (len (nouvelleBDD)-1): # On parcourt les donnees de tout le tableau
    voisinage.append (distance (coord1, coordonnees [nouvelleBDD [i]][0:4])) # On calcule toutes les distances entre le point choisi et le reste du tableau
  voisinTrouve = []
  for i in range (k):
    minDist = -np.inf
    for j in range (len (nouvelleBDD)-1): # On parcourt les donnees de tout le tableau
      if voisinage [j] != 0 and voisinage [j] < minDist and j not in voisinTrouve: # Si la distance calcule est differente de 0 et inferieur a la plus petite distance et que cette valeur n'est pas deja dans les points selectionnes
        minDist = voisinage [j] # Alors mindist prend la distance entre le point choisi et le point verifie
        indice = j
    voisinTrouve.append (indice) # Correspond au point le plus proche du point choisi
  return (voisinTrouve) # Retour les points qui sont les plus proches

# Permet de predire ce que doit etre le point du tableau en fonction de ses k voisins
def prediction (voisin):
  attribution = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'] # Liste des possibilites
  valeur = [0, 0, 0]
  for test in voisin : # Parcours le resultat des k voisins
    for i in range (3): 
      if coordonnees [test] [4] == attribution [i]: # Permet de connaitre combien il y a de voisins qui ont la meme possibilite
        valeur [i] += 1
  nombreValeur = 0 
  indice = 0
  for i in range (3): # Parcours les 3 cases presents dans valeur
    if valeur [i] > nombreValeur: # Permet de savoir quelle case present dans valeur est la plus eleve
      nombreValeur = valeur [i] 
      indice = i # L'indice correspond a la possibilite qui est presente chez la majorite des k voisins
  return (attribution [indice]) # Retour la possibilite presente chez la majorite des k voisins ce qui devient la possibilite du point teste

# Permet de connaitre le pourcentage d'erreur pour la prediction de l'attribution chez les points tests
def nombreErreur (k, pourcent):
    global nouvelleBDD # Initialisation d'une nouvelle base de donnee a partir de l'originale
    nombreElement = [i for i in range (len (coordonnees))] # Permet de copier la base originale
    nouvelleDonnee = int (pourcent * len(coordonnees)) # On prend une partie de la base comme reference pour le test
    shuffle (nombreElement) # On selectionne une partie au hasard de la nouvelle base
    nouvelleBDD = nombreElement [0:nouvelleDonnee] # La nouvelle base est defini en prenant en compte le pourcentage que l'on veut garder de la base originale
    baseTest = nombreElement [nouvelleDonnee:len(coordonnees)] # Une base a teste est cree avec ce qu'il reste de la nouvelle base
    predictionErreur = 0
    for j in baseTest: # On parcourt la base a teste
      if prediction (voisinProcheK2 (coordonnees [j][0:4], k)) != coordonnees [j][4]: # On cherche les k voisins des points a tester et on regarde si la prediction de leur attribut est bonne
        predictionErreur += 1
    print ((predictionErreur / len (baseTest)) * 100) # Retourne le pourcentage d'erreur sur l'ensemble de la base a teste


