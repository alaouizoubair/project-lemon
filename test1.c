#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <string.h>

int main(int argc, char *argv[])
{
	#ifndef _OPENMP
	#error OpenMP est absent
	#endif
	
	/* 
		argv[1] : nom du fichier à classer
		argv[2] : nb threads
		argv[3] : nb Modèles
	*/	
	if (argc == 4)
	{
		char *fileName = argv[1];
		int nbThreads=atoi(argv[2]);
		// n : nombre de modèles
		int n = atoi(argv[3]);
		/*
		printf("Nom du fichier : %s \n", fileName);
		printf("nb threads : %d \n", nbThreads);
		*/
		srand(time(NULL));
				
		double debutSeq = omp_get_wtime();
    	// A adapter, partie séquentielle, il faudrait traiter la valeur de retour à la volée
    	/*
    	for(int i=0;i<n;i++)
		{
				snprintf(cmdbuf, sizeof(cmdbuf), "python reco_face.py %s %d",fileName, i);				
				res = system(cmdbuf);
				//printf("Resultat : %d pour i = %d\n", res, i);
		}*/
		
		double finSeq = omp_get_wtime();
		double t1=finSeq-debutSeq;
		printf("Temps d'execution sequentiel avec n = %d : %f \n",n,t1);
		
		omp_set_num_threads(nbThreads);
		double debutPar =omp_get_wtime();
		char cmdbuf[256];
		int res;
		// Idem que précédemment, il faudrait soit traiter res à la volée, soit faire un reduce max dessus (plus tentant)
		// Puisque reco_face ne retourne pas la bonne valeur (limitation unix), nous n'avons pas traité outre mesure
		#pragma omp parallel
		{
			#pragma omp for
			for(int i=1;i<n;i++)
			{
				snprintf(cmdbuf, sizeof(cmdbuf), "python reco_face.py %s %d",fileName, i);				
				res = system(cmdbuf);
				//printf("Resultat : %d pour i = %d\n", res, i);
			}
			
		}
		double finPar = omp_get_wtime();
		double tp=finPar-debutPar;
		printf("Temps d'execution parallele avec nbThreads = %d  : %f\n",nbThreads,tp);
		
		printf("SpeedUp = %f \n",t1/tp);
		printf("Efficacité = %f \n",(t1/tp)/nbThreads);		
	}
	else
		printf("Erreur sur le nombre d'arguments du programme <nomFichier> <nombre de Threads>!! \n");
	return 0;
}
