!------------------README--------------------!
Le 02/02/2017
Développé par : Ashfack ABDOUL AZID, Zoubair ALAOUI, Mostapha BOUDJRAF
INGE INFO3 - GROUPE 7

1 - Programme séquentiel
	1.1 - Objectif
		Le programme séquentiel établit une reconnaissance faciale en comparant les pixels des photos de plusieurs personnes en déduisant le poucentage de ressemblance.
	1.2 - Exécution du programme
		$ mpicc imageCompSeq.c -o imageCompSeq
		$ gcc faceRecognitionSeq.c -o faceRecognitionSeq
		$ ./faceRecognitionSeq <nom_photo_personne_recherchée>


2 - Programme Distribué
	2.1 - Objectif
		L'objectif est le même qu'en séquentiel mais on le réalise en distribué
	2.2 - Exécution du programme
		$ mpicc imageComp.c -o imageComp
		$ gcc faceRecognition.c -o faceRecognition
		$ ./faceRecognition <nom_photo_personne_recherchée>

3.Remarques
	Les photos des personnes doivent figurer dans un répertoire nommé "photos"
	Chaque personne doit avoir son propre répertoire avec un nom sous cette forme "subjectX"
