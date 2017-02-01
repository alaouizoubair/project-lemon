try:
    from PIL import Image
except ImportError:
    import Image

import os

photos = os.getcwd()+'/photos/'
print(photos)
for subject in os.listdir(photos):
	cwd = photos+subject+'/'
	for imgName in os.listdir(cwd):
		img = Image.open(cwd+imgName)
		img = img.resize((1000,1000),Image.ANTIALIAS);
		img.save(cwd+imgName);
		print(imgName + " a été redimensioné")

