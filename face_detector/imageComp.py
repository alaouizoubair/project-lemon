try:
    from itertools import izip
except ImportError:
    izip = zip

try:
    from PIL import Image
except ImportError:
    import Image

import os, sys

#On récupère le chemin du répertoire de photos d'une personnes
try:
 	subjectPath = sys.argv[2]
except IndexError:
 	print("Aucun répertoire subject dans le second argument")

#Récupère l'image recherchée

try:
	imagePath = sys.argv[1]
except IndexError:
	print("L'image recherchée n'est pas indiquée dans les arguments")


#On ouvre le chemin vers la liste des photos de la personne concerné
cwd = os.getcwd()+'/photos/'+subjectPath+'/'

#Ouvrir l'image avec la librairie Image
i1 = Image.open(imagePath) #Open image to search for
bestfitpercent = 0 
bestfitpath= ""

#Itération sur la liste des photos d'une personnes
for imgName in os.listdir(cwd): 
	i2 = Image.open(cwd+imgName)

	assert i1.size == i2.size, "Different sizes." # S'assurer que la taille des photos est identique
	 
	#Algorithme qui cherche la différence entre la photo choisie et les photos dans la liste
	pairs = zip(i1.getdata(), i2.getdata()) 
	if len(i1.getbands()) == 1:
	    dif = sum(abs(p1-p2) for p1,p2 in pairs)
	else:
	    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
	 
	ncomponents = i1.size[0] * i1.size[1] * 3
	percent = (((dif / 255.0 * 100) / ncomponents)-100)*(-1)

	if(percent >= bestfitpercent):
		bestfitpercent = percent
		bestfitpath = cwd+imgName


print(bestfitpercent)
