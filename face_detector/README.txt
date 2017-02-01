!------------------README--------------------!
1 - Programme séquentiel
	1.1 - Objectif
		Le programme séquentiel établie une reconnaissance facial en comparant les pixels des photos de plusieurs personnes en déduisant le poucentage de ressemblance.
	1.2 - Exécution du programme
		$ gcc imageCompSeq.c -o imageCompSeq
		$ gcc faceRecognitionSeq.C -o faceRecognitionSeq
		$ ./faceRecognitionSeq <nom_photo_personne_recherchée>


2 - Programme Distribué
	2.1 - Objectif
		Le programme distribué établie une reconnaissance facial en comparant les pixels des photos de plusieurs personnes en déduisant le poucentage de ressemblance.
	2.2 - Exécution du programme
		$ mpicc imageComp.c -o imageComp
		$ gcc faceRecognition.C -o faceRecognition
		$ ./faceRecognition <nom_photo_personne_recherchée>

3.Remarques
	Les photos des personnes doivent figurer dans un répertoire nommé "photos"
	Chaque personne doit avoir son propre répertoire avec un nom sous cette forme "subjectX"

		