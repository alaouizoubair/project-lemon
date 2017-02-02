# -*- coding: utf-8 -*-
from mpi4py import MPI
from reco_face import compete
import sys

# a executer avec nb processus = nb de modèles
# on donne le chemin du fichier à classer dans argv[1]
# on considère que les modèles sont numérotés à partir de 1
if __name__ == '__main__':	
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	nbModels = comm.Get_size()
	start_time = MPI.Wtime()
	label, risk = compete(sys.argv[1], rank+1)
	minRisk = comm.allreduce(risk,0,MPI.MIN)
	end_time = MPI.Wtime()
	print("--- %s secondes, label %d et risque %d ---" % (end_time - start_time, label, risk))
	if risk == minRisk:
		print ("le gagnant est : %d" % label)
	
	""" Partie 'séquentielle' """
	if rank == 0:
		start_timeS = MPI.Wtime()
		bestLabel = -1
		minRisk = 101
		for i in range(nbModels):
			label, risk = compete(sys.argv[1], i+1)
			if minRisk > risk:
				minRisk = risk
				bestLabel = label
						
		end_timeS = MPI.Wtime()
		print("--- %s secondes en séquentiel, label %d et risque %d ---" % (end_timeS - start_timeS, bestLabel, minRisk))	
		speedUp = (end_timeS - start_timeS)/(end_time - start_time)
		print("SpeedUp : %f" % (speedUp))
		print("Travail : %f" %( nbModels*(end_time - start_time)))
		print("Efficacité : %f" % (speedUp/ nbModels))
		
