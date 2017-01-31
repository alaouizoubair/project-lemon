# -*- coding: utf-8 -*-
#!/usr/bin/python

# Imports
import cv2, os
import numpy as np
from PIL import Image
import sys
from mpi4py import MPI
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

def get_images_and_labels(image_paths):
    """
    Image paths est l'ensemble d'apprentissage
    """
    images = []
    # labels ou classe pour le classifieur d'open CV , sera un entier
    labels = []
    for image_path in image_paths:
        # Conversion en nuances de gris
        image_pil = Image.open(image_path).convert('L')
        # Conversion en numpy array
        image = np.array(image_pil, 'uint8')
        # Le label
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        # Detection du visage
        faces = faceCascade.detectMultiScale(image)
        # Si l'image est trouvée ...
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
            # Pour afficher l'ajout d'images
            cv2.imshow("Ajout de têtes au modèle d'apprentissage ....", image[y: y + h, x: x + w])
            cv2.waitKey(50)
    # retourne les listes d'images et labels
    return images, labels


# argv[1] : numéro du répertoire si utilisation en mode manuel
if __name__ == '__main__':
	# Utilisation de LBPH Face Recognizer 
	recognizer = cv2.createLBPHFaceRecognizer()
	
	fileNames = sys.argv[1:]
	comm = MPI.COMM_WORLD
	size = comm.Get_size()
	nbModels = size
	rank = comm.Get_rank()
	nbFilesPerModel = int(len(fileNames)/size)
	
	# Chaque processus va avoir nbFilesPerModel dans son modèle, sauf le dernier processus, qui aura ce qui reste
	# Chaque processus aura les fichiers de rank*nbFilesPerModel à (rank+1) * nbFilesPerModel -1
	
	start_time = MPI.Wtime()
	if(rank != size -1):
		print('process', rank, 'treating',rank*nbFilesPerModel,'-',(rank+1) * nbFilesPerModel)
		images, labels = get_images_and_labels(fileNames[rank*nbFilesPerModel : (rank+1) * nbFilesPerModel])
		
	else:
		print('process', rank, 'treating',rank*nbFilesPerModel)
		images, labels = get_images_and_labels(fileNames[rank*nbFilesPerModel:])
	cv2.destroyAllWindows()
	recognizer.train(images, np.array(labels))
	recognizer.save("./model" + str(rank+1) + ".xml")
	end_time = MPI.Wtime()
	if(rank == size -1):
		print("--- %s secondes en parallèle---" % (end_time - start_time))
	# Pour éviter d'influer sur le temps de la partie séquentielle
	comm.Barrier()
	""" Partie 'séquentielle' """
	if rank == 0:
		start_timeS = MPI.Wtime()
		for i in range(nbModels-1):
			images, labels = get_images_and_labels(fileNames[i*nbFilesPerModel : (i+1) * nbFilesPerModel])
			cv2.destroyAllWindows()
			recognizer.train(images, np.array(labels))
			recognizer.save("./model" + str(i+1) + ".xml")
		images, labels = get_images_and_labels(fileNames[(nbModels-1)*nbFilesPerModel:])
		cv2.destroyAllWindows()
		recognizer.train(images, np.array(labels))
		recognizer.save("./model" + str(nbModels) + ".xml")	
		end_timeS = MPI.Wtime()
		print("--- %s secondes en séquentiel---" % (end_timeS - start_timeS))	
		speedUp = (end_timeS - start_timeS)/(end_time - start_time)
		print("SpeedUp : %f" % (speedUp))
		print("Travail : %f" %( nbModels*(end_time - start_time)))
		print("Efficacité : %f" % (speedUp/ nbModels))
		

