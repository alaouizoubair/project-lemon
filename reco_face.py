# -*- coding: utf-8 -*-
#!/usr/bin/python

# Imports
import cv2, os
import numpy as np # pour que la data soit conforme (entier entre 0 et 255)
from PIL import Image # pour convertir l'image en nuances de gris
import sys


def compete(filePath, modelNumber):
	cascadePath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascadePath)
	
	recognizer = cv2.createLBPHFaceRecognizer()

	modelPath = './model' + str(modelNumber) + ".xml"
	recognizer.load(modelPath)
	
	predict_image_pil = Image.open(filePath).convert('L')
	predict_image = np.array(predict_image_pil, 'uint8')
	faces = faceCascade.detectMultiScale(predict_image)
	
	for (x, y, w, h) in faces:
	    nbr_predicted, risk = recognizer.predict(predict_image[y: y + h, x: x + w])
	    #print(nbr_predicted, int(risk))
	return(int(nbr_predicted), int(risk))
	""" 
	Si on veut essayer d'utiliser avec C, cela peut être une bonne piste
	On crée une sorte de mapping
	En faisant z = risk * 101 + nbr_predicted, on peut retrouver risk et nbr_predicted 
	en jouant sur le modulo et la partie entiere
	"""
	#return(int(risk)*101 + nbr_predicted)

# argv[1] : chemin de l'image à classifier
# argv[2] : numéro du modèle
if __name__ == '__main__':
	sys.exit(compete(sys.argv[1], sys.argv[2]))
