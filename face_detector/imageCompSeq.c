#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <python3.5/Python.h>
#include <string.h>

/*******************************/
/* argv[1] : <nom_photo>       */
/* argv[2:n] : <subject_list>  */
/*******************************/

int main(int argc,char** argv){

    FILE *fp;
    char cmd[100];
	char path[1035];
	int rank,size,i,d=0;
	double maxglob=-1,max; 
	

	// Cette boucle traverse tous les répertoires de photos des personnes que nous avons
	for(i=0;i<argc-2;i++){
		
		// Création de la commande pour trouver le pourcentage de ressemblance par rapport aux photos d'une personne
		sprintf(cmd,"python imageComp.py %s %s\n",argv[1],argv[i+2]);
		
		// Exécution de la commande
		fp = popen(cmd, "r");
		if (fp == NULL) {
			printf("Failed to run command\n" );
			exit(1);
		}

		// Récupérer le pourcentage retourner par le script python
		fgets(path, sizeof(path)-1, fp);
		pclose(fp);


		max = atof(path);
		// A chaque itération, nous comparons la valeur maximum avec la nouvelle valeur, et nous gardons la plus grande
		if(maxglob<max || maxglob ==-1){
			maxglob = max;
			d=i;
		}
	}

	//Afficher le bilan de la recherche en retournant la personne la plus plausible
	printf("/******************************************/\n=>Programme tourné en séquentiel\n=>Nombre de processus utilisés: 1\n=>Pourcentage de ressemblance: %.2f % \n=>Source: subject%d\n",maxglob,d+1);


	return 0;
}
