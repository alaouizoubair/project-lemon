#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <python3.5/Python.h>
#include <string.h>
#include <mpi.h>

/*******************************/
/* argv[1] : <nom_photo>       */
/* argv[2:n] : <subject_list>  */
/*******************************/

int main(int argc,char** argv){

    FILE *fp;
    char cmd[100];
	char path[1035];
	MPI_Status status;
	int rank,size,d;
	double max,maxglob; 
	int root=0;

	// On initialize MPI
	MPI_Init(&argc,&argv);
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&size);


	assert(argc-2 == size);

	// Command to launch the python script

	sprintf(cmd,"python imageComp.py %s %s\n",argv[1],argv[rank+2]);
	

	//Exécution de la commande
	fp = popen(cmd, "r");
	if (fp == NULL) {
		printf("Echec de l'exécution\n" );
		exit(1);
	}

	fgets(path, sizeof(path)-1, fp);
	pclose(fp);

	//Récupérer le maximum local
	max = atof(path);
	
	// On transmet à tous les processus les maximums locaux pour avoir le maximum global
	MPI_Allreduce(&max,&maxglob,1,MPI_DOUBLE,MPI_MAX,MPI_COMM_WORLD);


	// Le processus ayant le max global envoie son id au processus root/mère
	if(maxglob == max){
		//printf("winner is me: %d\n",rank);
		MPI_Send(&rank,1,MPI_INT,0,0,MPI_COMM_WORLD);
		
	}

	// Le processus root récupère le numéro du processus ayant le max global
	if(rank==root){
		MPI_Recv(&d,1,MPI_INT,MPI_ANY_SOURCE,0,MPI_COMM_WORLD,&status);
		printf("/******************************************/\n=>Programme tourné en distribué\n=>Nombre de processus utilisés: %d\n=>Pourcentage de ressemblance: %.2f % \n=>Source: subject%d\n",size,maxglob,d+1);
	}



	
	MPI_Finalize();
	
	return 0;
}
