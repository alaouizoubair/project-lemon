#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <python3.5/Python.h>
#include <time.h>

/***************************/
/* argv[1] : <nom_photo>   */
/***************************/

int main(int argc, char**argv){

	FILE *fp;
	char subject_list[1035],result[1035];
	char number[5];
	char cmd[1024];
	int cpt=0,i;
	time_t start_t, end_t;
   	double diff_t;

   	if (argc != 2) {
		printf("Usage: %s <nom_photo>\n",argv[0]);
		exit(1);
	}

   	// Nous listons les répertoires des sujets et nous enregistrons le résultat(char*) dans subject_list
	fp = popen("ls photos/ | tr \"\n\" \" \"", "r");
	if (fp == NULL) {
		printf("Failed to run command\n" );
		exit(1);
	}

	assert(fgets(subject_list, sizeof(subject_list)-1, fp) != NULL);

	pclose(fp);

	//Nous récupèrons le nombre de répertoires et nous enregistrons le résultat(int) dans la variable cpt
	fp = popen("ls photos| wc -l", "r");
	if (fp == NULL) {
		printf("Failed to run command\n" );
		exit(1);
	}

	assert(fgets(number, sizeof(number)-1, fp) != NULL);
	cpt = atoi(number);
	
	pclose(fp);


	// Création de la commande qui lance le programme MPI en c (imageComp.c) avec un nombre de processus égal au nombre de sujet existant
	sprintf(cmd,"./imageCompSeq %s %s",argv[1],subject_list);
	fp=popen(cmd, "r");
	// Début du timer
	time(&start_t);	
	// Exécution de la partie cherchant le meilleur pourcentage (Séquentiel)
	fp = popen(cmd, "r");
	if (fp == NULL) {
		printf("Failed to run command\n" );
		exit(1);
	}

	// Nous récupérons le résultat retourné du programme "imageComp"
	while (fgets(result, sizeof(result)-1, fp) != NULL) {
		printf("%s", result);
	}

	// Fin du timer
	time(&end_t);

	// Nous calculons le temps d'exécution
	diff_t = difftime(end_t, start_t);

	//Affichage du temps d'exécution 
	printf("=>Temps d'exécution (Algo Séquentiel): %.2f secondes\n/******************************************/\n",diff_t);

	

	return 0;
}