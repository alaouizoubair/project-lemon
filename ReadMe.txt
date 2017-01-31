/* Pour lancer */

/* 1. Pour les modèles : nb nombre de modèles désirés, fileList est la liste avec nom des fichiers à apprendre 
	les fichiers doivent respecter la convention de nom suivante : subjectNUMBER.peuImporte,
	si deux fichiers ont le même number, alors le programme considère que c'est la même personne
*/ 

mpiexec -n <nb> python gen_models_distributed.py <fileList>
/* Exemple */
mpiexec -n 10 python gen_models_distributed.py training_data/*


/* 2. Pour la prédiction : 
	filePath est le chemin du fichier à classifier, 
	nb est le nombre de modèles et le nombre de processus (idéalement), mais il ne doit pas être supérieur au nombre de modèles
*/

mpiexec -n <nb> python mpi.py <filePath>
/* Exemple */
mpiexec -n 10 python mpi.py test_data/subject03.sad


/* Partie non fonctionnelle, mais qui peut être testée */
3. Pour tester avec le C
 --> Changer la valeur de retour dans reco_face pour que ce soit une seule valeur qui puisse être lue par popen, ou utilser un print
 -- Test1 : avec command system
 -- Test2 : avec popen
 
4. Pour lancer le C :
make test1
make test2
/*
	filePath est le chemin du fichier à classifier, 
	nbThreads est le nombre de threads 
	nbModels est le nombre de modèles
*/
./test1 <filePath> <nbThreads> <nbModels>
./test2 <filePath> <nbThreads> <nbModels>
./test1 test_data/subject01.sad 7 10
./test2 test_data/subject01.sad 7 10
