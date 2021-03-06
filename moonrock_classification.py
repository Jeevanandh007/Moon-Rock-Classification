# -*- coding: utf-8 -*-
"""MOONROCK Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12NioQHmgqOnB33p5PTqsb5Cz7xxyIiBu
"""

from google.colab import drive
drive.mount('/content/drive')

import tensorflow as tf
import os
import zipfile
local_zip = '/content/drive/My Drive/Train Images.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content/Train Images')
local_zip ='/content/drive/My Drive/Validation Images.zip'
zip_ref = zipfile.ZipFile(local_zip,'r')
zip_ref.extractall('/content/Validation Images')
local_zip ='/content/drive/My Drive/Test Images.zip'
zip_ref = zipfile.ZipFile(local_zip,'r')
zip_ref.extractall('/content/Test Images')


zip_ref.close()

train_large_dir = os.path.join('/content/Train Images/Train Images/Large')

train_small_dir= os.path.join('/content/Train Images/Train Images/Small')

print('total training Large images:', len(os.listdir(train_large_dir)))
print('total training Small images:', len(os.listdir(train_small_dir)))

validation_large_dir = os.path.join('/content/Validation Images/Validation Images/Large')

validation_small_dir = os.path.join('/content/Validation Images/Validation Images/Small')

print('total validating Large images:',len(os.listdir(validation_large_dir)))
print('total validating Small images:',len(os.listdir(validation_small_dir)))

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255,
                                  rotation_range=40,
                                  width_shift_range=0.2,
      height_shift_range=0.2,
      horizontal_flip=True,)

train_generator = train_datagen.flow_from_directory(
        '/content/Train Images/Train Images',  
        target_size=(300, 300),  
        batch_size=128,
      
        class_mode='binary')

validation_datagen = ImageDataGenerator(rescale =1./255)
validation_generator = validation_datagen.flow_from_directory('/content/Validation Images/Validation Images',target_size=(300,300),batch_size=28,class_mode= 'binary')

model = tf.keras.models.Sequential([
    
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(300, 300, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
  
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
  
  
    tf.keras.layers.Flatten(),
    
    tf.keras.layers.Dense(512, activation='relu'),
    
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.summary()

from tensorflow.keras.optimizers import RMSprop

model.compile(loss='binary_crossentropy',
              optimizer='AdaGrad',
              metrics=['acc'])

history = model.fit_generator(
      train_generator,
      steps_per_epoch=5,  
      epochs=15,
      verbose=1,
      validation_data = validation_generator,
      validation_steps =10)

import numpy as np
from google.colab import files
from keras.preprocessing import image
import pandas as pd

filenames = pd.read_csv('/content/test.csv')

df = pd.DataFrame(columns=['Image_File', 'Class'])
for file in filenames['Image_File']:

    fn=file

  
    path = '/content/Test Images/Test Images/'+fn
    img = image.load_img(path, target_size=(300, 300))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = model.predict(images, batch_size=50)
  
    if classes[0]>0.5:
      print(fn + ",Small")
      df = df.append({'Image_File': fn,'Class': 'Small'}, ignore_index=True)
      
    else:
      print(fn + ",Large")
      df = df.append({'Image_File': fn,'Class': 'Large'}, ignore_index=True)

df.to_csv('Output.csv')