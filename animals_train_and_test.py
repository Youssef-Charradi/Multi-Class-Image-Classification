# -*- coding: utf-8 -*-
"""Animals-train and test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aPCP2d5re6G3T88ssPsYQdHeqzosK_eP
"""

!unzip drive/MyDrive/Colab_Notebooks/Image_reconaissance/donnees.zip

import shutil, os
import random

animal=['elephant','girafe','leopard','rhino','tigre','zebre']
list_of_indexes = random.sample(range(1,4001), 400)
for i,ind in enumerate(list_of_indexes) :
  if ind<10:
    list_of_indexes[i]='000'+str(ind)
  elif ind<100:
    list_of_indexes[i]='00'+str(ind)
  elif ind<1000:
    list_of_indexes[i]='0'+str(ind)
  else:
    list_of_indexes[i]=str(ind)
 
print(list_of_indexes)

for ani in animal:
  end='donnees/validation/'+ani
  for ind in list_of_indexes:
    start='donnees/entrainement/'+ani+'/'+ind+'.png'
    shutil.move(start,end)

# ==========================================
# ======CHARGEMENT DES LIBRAIRIES===========
# ==========================================

import numpy as np

# La libraire responsable du chargement des données dans la mémoire

from keras.preprocessing.image import ImageDataGenerator

# Le Type de notre modéle (séquentiel)

from keras.models import Model
from keras.models import Sequential

# Le type d'optimisateur utilisé dans notre modèle (RMSprop, adam, sgd, adaboost ...)
# L'optimisateur ajuste les poids de notre modèle par descente du gradient
# Chaque optimisateur a ses propres paramètres
# Note: Il faut tester plusieurs et ajuster les paramètres afin d'avoir les meilleurs résultats

from keras.optimizers import Adam, Nadam

# Les types des couches utlilisées dans notre modèle
from keras.layers import Conv2D, MaxPooling2D, Input, BatchNormalization, UpSampling2D, Activation, Dropout, Flatten, Dense

# Des outils pour suivre et gérer l'entrainement de notre modèle
from keras.callbacks import CSVLogger, ModelCheckpoint, EarlyStopping

# Configuration du GPU
import tensorflow as tf
from keras import backend as K

# Sauvegarde du modèle
from keras.engine.saving import load_model

# Affichage des graphes 
import matplotlib.pyplot as plt

from tensorflow import keras
from keras.utils import to_categorical
from keras import optimizers

# ==========================================
# ===============GPU SETUP==================
# ==========================================

# Configuration des GPUs et CPUs
config = tf.compat.v1.ConfigProto(device_count={'GPU': 2, 'CPU': 4})
sess = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(sess);

#shutil.rmtree('donnees/entrainement') 
#shutil.rmtree('donnees/validation') 
#shutil.rmtree('donnees/test')
#shutil.rmtree('donnees')

# ==========================================
# ================VARIABLES=================
# ==========================================

# ******************************************************
#                       QUESTION DU TP
# ******************************************************
# 1) Ajuster les variables suivantes selon votre problème:
# - mainDataPath
# - training_batch_size
# - validation_batch_size
# - image_scale
# - image_channels
# - images_color_mode
# - fit_batch_size
# - fit_epochs
# ******************************************************

# Le dossier principal qui contient les données
mainDataPath = "donnees/"

# Le dossier contenant les images d'entrainement
trainPath = mainDataPath + "entrainement"

# Le dossier contenant les images de validation
validationPath = mainDataPath + "test"

# Le dossier contenant les images de test
testPath = mainDataPath + "test"

# Le nom du fichier du modèle à sauvegarder
modelsPath = "Model.hdf5"
animal=['elephant','girafe','leopard','rhino','tigre','zebre']

# Le nombre d'images d'entrainement et de validation
# Il faut en premier lieu identifier les paramètres du CNN qui permettent d’arriver à des bons résultats. À cette fin, la démarche générale consiste à utiliser une partie des données d’entrainement et valider les résultats avec les données de validation. Les paramètres du réseaux (nombre de couches de convolutions, de pooling, nombre de filtres, etc) devrait etre ajustés en conséquence.  Ce processus devrait se répéter jusqu’au l’obtention d’une configuration (architecture) satisfaisante. 
# Si on utilise l’ensemble de données d’entrainement en entier, le processus va être long car on devrait ajuster les paramètres et reprendre le processus sur tout l’ensemble des données d’entrainement.


training_batch_size = 24000  # total 24000  (4000 par classe)
validation_batch_size = 6000  # total 6000 (1000 par classe)

# Configuration des  images 
image_scale = 160 # la taille des images
image_channels = 3  # le nombre de canaux de couleurs (1: pour les images noir et blanc; 3 pour les images en couleurs (rouge vert bleu) )
images_color_mode = "rgb"  # grayscale pour les image noir et blanc; rgb pour les images en couleurs 
image_shape = (image_scale, image_scale, image_channels) # la forme des images d'entrées, ce qui correspond à la couche d'entrée du réseau

# Configuration des paramètres d'entrainement
fit_batch_size = 32 # le nombre d'images entrainées ensemble: un batch
fit_epochs = 15 # Le nombre d'époques

# ==========================================
# =r================MODÈLE==================
# ==========================================

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                       QUESTIONS DU TP
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Ajuster les deux fonctions:
# 2) feature_extraction
# 3) fully_connected
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#Couche d'entrée:
# Cette couche prend comme paramètre la forme des images (image_shape)
input_layer = Input(shape=image_shape)


# Partie feature extraction (ou cascade de couches d'extraction des caractéristiques)
def feature_extraction(input):
  
    # 1-couche de convolution avec nombre de filtre  (exp 32)  avec la taille de la fenetre de ballaiage exp : 3x3 
    # 2-fonction d'activation exp: sigmoid, relu, tanh ...
    # 3-couche d'echantillonage (pooling) pour reduire la taille avec la taille de la fenetre de ballaiage exp :2x2  
    
    # **** On répète ces étapes tant que nécessaire ****
    
    #layer1
    x = Conv2D(64, (3, 3), padding='same')(input) 
    x = Activation("relu")(x) 

    x = MaxPooling2D((2, 2), padding='same')(x)
    
    #layer2    
    x = Conv2D(128, (3, 3), padding='same')(x)
    x = Activation("relu")(x)

    x = MaxPooling2D((2, 2), padding='same')(x) 

    #layer2    
    x = Conv2D(256, (3, 3), padding='same')(x)
    x = Activation("relu")(x)

    x = MaxPooling2D((2, 2), padding='same')(x) 


    #layer4
    x = Conv2D(512, (3, 3), padding='same')(x)
    x = Activation("relu")(x)

    x = MaxPooling2D((2, 2), padding='same')(x)  
    

    #layer5
    x = Conv2D(1024, (3, 3), padding='same')(x)
    x = Activation("relu")(x)

    encoded = MaxPooling2D((2, 2), padding='same')(x)  
    return encoded

# Partie complètement connectée (Fully Connected Layer)
def fully_connected(encoded):
    # Flatten: pour convertir les matrices en vecteurs pour la couche MLP
    # Dense: une couche neuronale simple avec le nombre de neurone (exemple 64)
    # fonction d'activation exp: sigmoid, relu, tanh ...
    x = Flatten(input_shape=image_shape)(encoded)
    x = Activation("relu")(x)
   

    x = Dense(168)(x)
    x = Activation("relu")(x)
  
    # Puisque'on a une classification binaire, la dernière couche doit être formée d'un seul neurone avec une fonction d'activation sigmoide
    # La fonction sigmoide nous donne une valeur entre 0 et 1
    # On considère les résultats <=0.5 comme l'image appartenant à la classe 0 (c.-à-d. la classe qui correspond au chiffre 2)
    # on considère les résultats >0.5 comme l'image appartenant à la classe 0 (c.-à-d. la classe qui correspond au chiffre 7)
    x = Dense(6)(x)
    sortie = Activation('softmax')(x)
    return sortie


# Déclaration du modèle:
# La sortie de l'extracteur des features sert comme entrée à la couche complétement connectée
model = Model(input_layer, fully_connected(feature_extraction(input_layer)))

# Affichage des paramétres du modèle
# Cette commande affiche un tableau avec les détails du modèle 
# (nombre de couches et de paramétrer ...)
model.summary()

# Compilation du modèle :
# On définit la fonction de perte (exemple :loss='binary_crossentropy' ou loss='mse')
# L'optimisateur utilisé avec ses paramétres (Exemple : optimizer=adam(learning_rate=0.001) )
# La valeur à afficher durant l'entrainement, metrics=['accuracy'] 
optimizer = 'adam'
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# ==========================================
# ==========CHARGEMENT DES IMAGES===========
# ==========================================

# training_data_generator: charge les données d'entrainement en mémoire
# quand il charge les images, il les ajuste (change la taille, les dimensions, la direction ...) 
# aléatoirement afin de rendre le modèle plus robuste à la position du sujet dans les images
# Note: On peut utiliser cette méthode pour augmenter le nombre d'images d'entrainement (data augmentation)
training_data_generator = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True)

# validation_data_generator: charge les données de validation en memoire
validation_data_generator = ImageDataGenerator(rescale=1. / 255)

# training_generator: indique la méthode de chargement des données d'entrainement
training_generator = training_data_generator.flow_from_directory(
    trainPath, # Place des images d'entrainement
    color_mode=images_color_mode, # couleur des images
    target_size=(image_scale, image_scale),# taille des images
    batch_size=training_batch_size, # nombre d'images à entrainer (batch size)
    classes=animal,  
    class_mode='categorical', # 6 classes
    shuffle=True) # on "brasse" (shuffle) les données -> pour prévenir le surapprentissage

# validation_generator: indique la méthode de chargement des données de validation
validation_generator = validation_data_generator.flow_from_directory(
    validationPath, # Place des images de validation
    color_mode=images_color_mode, # couleur des images
    target_size=(image_scale, image_scale),  # taille des images
    batch_size=validation_batch_size,  # nombre d'images à valider
    classes=animal,  
    class_mode='categorical', # 6 classes
    shuffle=True) # on "brasse" (shuffle) les données -> pour prévenir le surapprentissage

# On imprime l'indice de chaque classe (Keras numerote les classes selon l'ordre des dossiers des classes)

print(training_generator.class_indices)
print(validation_generator.class_indices)

# On charge les données d'entrainement et de validation
# x_train: Les données d'entrainement
# y_train: Les Ètiquettes des données d'entrainement
# x_val: Les données de validation
# y_val: Les Ètiquettes des données de validation

(x_train, y_train) = training_generator.next()
(x_val, y_val) = validation_generator.next()

# ==========================================
# ==============ENTRAINEMENT================
# ==========================================

# Savegarder le modèle avec la meilleure validation accuracy ('val_acc') 
# Note: on sauvegarder le modèle seulement quand la précision de la validation s'améliore
modelcheckpoint = ModelCheckpoint(filepath=modelsPath,
                                  monitor='val_accuracy', verbose=1, save_best_only=True, mode='auto')

# entrainement du modèle
classifier = model.fit(x_train, y_train,
                       epochs=fit_epochs, # nombre d'époques
                       batch_size=fit_batch_size, # nombre d'images entrainées ensemble
                       validation_data=(x_val, y_val), # données de validation
                       verbose=1, # mets cette valeur ‡ 0, si vous voulez ne pas afficher les détails d'entrainement
                       callbacks=[modelcheckpoint], # les fonctions à appeler à la fin de chaque époque (dans ce cas modelcheckpoint: qui sauvegarde le modèle)
                       shuffle=True)# shuffle les images

# ==========================================
# ========AFFICHAGE DES RESULTATS===========
# ==========================================

# ***********************************************
#                    QUESTION
# ***********************************************
#
# 4) Afficher le temps d'execution
#
# ***********************************************

# Plot accuracy over epochs (precision par époque)
print(classifier.history.keys())
plt.plot(classifier.history['accuracy'])
plt.plot(classifier.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'])
fig = plt.gcf()
plt.show()

# ***********************************************
#                    QUESTION
# ***********************************************
#
# 5) Afficher la courbe d’exactitude par époque (Training vs Validation) ainsi que la courbe de perte (loss)
#
# ***********************************************

# ==========================================
# ==================MODÈLE==================
# ==========================================

#Chargement du modéle sauvegardé dans la section 1 via 1_Modele.py
model_path = "Model.hdf5"
Classifier: Model = load_model(model_path)

# ==========================================
# ================VARIABLES=================
# ==========================================

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                       QUESTIONS
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 1) A ajuster les variables suivantes selon votre problème:
# - mainDataPath         
# - number_images        
# - number_images_class_x
# - image_scale          
# - images_color_mode    
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# L'emplacement des images de test
mainDataPath = "donnees/"
testPath = mainDataPath + "test"

# Le nombre des images de test à évaluer
number_images = 6000 
number_images_class = 1000

# ==========================================
# =========CHARGEMENT DES IMAGES============
# ==========================================

# Chargement des images de test
test_data_generator = ImageDataGenerator(rescale=1. / 255)

test_itr = test_data_generator.flow_from_directory(
    testPath,# place des images
    target_size=(image_scale, image_scale), # taille des images
    classes=animal,  
    class_mode='categorical',# Type de classification
    shuffle=False,# pas besoin de les boulverser
    batch_size=1,# on classe les images une à la fois
    color_mode=images_color_mode)# couleur des images

(x, y_true) = test_itr.next()

y_true = np.array([0] * number_images_class + 
                  [1] * number_images_class +
                  [2] * number_images_class +
                  [3] * number_images_class +
                  [4] * number_images_class +
                  [5] * number_images_class )
y_true=to_categorical(y_true)

# evaluation du modËle
test_eval = Classifier.evaluate_generator(test_itr, verbose=1)

# Affichage des valeurs de perte et de precision
print('>Test loss (Erreur):', test_eval[0])
print('>Test précision:', test_eval[1])

# Prédiction des classes des images de test
predicted_classes = Classifier.predict_generator(test_itr, verbose=1)
predicted_classes_perc = np.round(predicted_classes.copy(), 4)
predicted_classes = np.round(predicted_classes) # on arrondie le output

# Cette list contient les images bien classées
correct = []
incorrect = []
for i in range(0, len(predicted_classes) ):
    
    if (predicted_classes[i]==y_true[i]).all():
      correct.append(i)
    else:
      incorrect.append(i)

# Nombre d'images bien classées
print("> %d  Ètiquettes bien classÈes" % len(correct))
print("> %d Ètiquettes mal classÈes" % len(incorrect))




# ***********************************************
#                  QUESTIONS
# ***********************************************
#
# 1) Afficher la matrice de confusion
# 2) Extraire une image mal-classée pour chaque combinaison d'espèces - Voir l'exemple dans l'énoncé.
# ***********************************************

