# -*- coding: utf-8 -*-
"""Plants_Leaf_Multiclass_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1muJ78Njtoe1_tAIxX21-qoih628VTXqh
"""


import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import numpy as np
import os
from glob import glob
import matplotlib.pyplot as plt

# Download the Data through Kaggle API
from google.colab import files

# Using Kaggle API to Download the Dataset

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))
  
# Then move kaggle.json into the folder where the API expects to find it.
!mkdir -p ~/.kaggle/ && mv kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json

# Download the Dataset
!kaggle datasets download -d csafrit2/plant-leaves-for-image-classification

from zipfile import ZipFile
file_name = "/content/plant-leaves-for-image-classification.zip"
with ZipFile(file_name,'r') as zip:
  zip.extractall()
  print('Done')
  zip.extractall(path="/content")

# We send some random train images from each and every classes to test folder with respective of classes
# It will help us to dataset imbalance to preventing from overfitting

import os
import shutil
import random

train_path = "/content/Plants_2/train/"  
test_path = "/content/Plants_2/test/"  
test_size = 0.2 # fraction of images to move to test folder

for folder_name in os.listdir(train_path):
    folder_path = os.path.join(train_path, folder_name)
    if os.path.isdir(folder_path):
        test_folder_path = os.path.join(test_path, folder_name)
        if not os.path.exists(test_folder_path):
            os.makedirs(test_folder_path)
        filenames = os.listdir(folder_path)
        random.shuffle(filenames)
        test_count = int(len(filenames) * test_size)
        test_files = filenames[:test_count]
        for file_name in test_files:
            file_path = os.path.join(folder_path, file_name)
            shutil.move(file_path, os.path.join(test_folder_path, file_name))

train_path = "/content/Plants_2/train/"  
test_path = "/content/Plants_2/test/"

for folder_path in [train_path, test_path]:
    print('Folder:', folder_path)
    # Iterate through each subfolder
    for subfolder_name in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder_name)
        # Count the number of images in the subfolder
        num_images = len(os.listdir(subfolder_path))
        print('    Subfolder:', subfolder_name, '- Num images:', num_images)

import os
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Define the number of random images to display from each subfolder
num_images_to_display = 1

# Iterate through the train and test folders
for folder_path in [train_path, test_path]:
    print('Folder:', folder_path)
    # Iterate through each subfolder
    for subfolder_name in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder_name)
        # Count the number of images in the subfolder
        num_images = len(os.listdir(subfolder_path))
        # Select some random images to display
        image_names = random.sample(os.listdir(subfolder_path), num_images_to_display)
        # Display the images
        for image_name in image_names:
            image_path = os.path.join(subfolder_path, image_name)
            image = mpimg.imread(image_path)
            plt.imshow(image)
            plt.rcParams['text.color'] = 'white'
            plt.tick_params(axis='x', colors='white')
            plt.tick_params(axis='y', colors='white')
            plt.title(subfolder_name)
            plt.show()

batch_size = 64
img_height = 224
img_width = 224

diseases = os.listdir(train_path)
print(diseases)

print("Total disease classes are: {}".format(len(diseases)))

plants = []
NumberOfDiseases = 0
for plant in diseases:
    if plant.split(' ')[0] not in plants:
        plants.append(plant.split(' ')[0])
    if plant.split(' ')[1] != 'healthy':
        NumberOfDiseases += 1

print(f"Unique Plants are: \n{plants}")

print("Number of plants: {}".format(len(plants)))

# Number of images for each disease
import pandas as pd
nums = {}
for disease in diseases:
    nums[disease] = len(os.listdir(train_path + '/' + disease))
    
# converting the nums dictionary to pandas dataframe passing index as plant name and number of images as column

img_per_class = pd.DataFrame(nums.values(), index=nums.keys(), columns=["no. of images"])
img_per_class

# plotting number of images available for each disease
index = [n for n in range(22)]
plt.figure(figsize=(20, 5))
plt.bar(index, [n for n in nums.values()], width=0.3)
plt.xlabel('Plants/Diseases', fontsize=13, color='white')
plt.ylabel('No of images available', fontsize=10, color='white')
plt.xticks(index, diseases, fontsize=10, rotation=90, color='white')
plt.title('Images per each class of plant disease', color='white')
plt.gca().spines['bottom'].set_color('white')
plt.gca().spines['top'].set_color('white')
plt.gca().spines['right'].set_color('white')
plt.gca().spines['left'].set_color('white')
plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')
plt.show()

import glob
def get_files(directory):
  if not os.path.exists(directory):
    return 0
  count=0
  # crawls inside folders
  for current_path,dirs,files in os.walk(directory):
    for dr in dirs:
      count+= len(glob.glob(os.path.join(current_path,dr+"/*")))
  return count
train_path ="/content/Plants_2/train"
test_path="/content/Plants_2/test"

#train file image count
train_samples =get_files(train_path)
#to get tags
num_classes=len(glob.glob(train_path+"/*")) 
#test file image count
test_samples=get_files(test_path)
print(num_classes,"Classes")
print(train_samples,"Train images")
print(test_samples,"Test images")

import pathlib
train_dir = "/content/Plants_2/train/"
data_dir = pathlib.Path(train_dir)

train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

test_dir = "/content/Plants_2/test"
data_dir = pathlib.Path(test_dir)

val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

n_train = 0
for value in nums.values():
    n_train += value
print(f"There are {n_train} images for training")

# Visualize the data
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 15))
for images, labels in train_ds.take(1):
  for i in range(15):
    ax = plt.subplot(5, 5, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")
    plt.rcParams['text.color'] = 'white'
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')


plt.subplots_adjust(wspace=0.1, hspace=0.7)
plt.show()

for image_batch, labels_batch in train_ds:
  print(image_batch.shape)
  print(labels_batch.shape)
  break

# Configure the dataset for performance
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

from tensorflow import keras
from tensorflow.keras import layers
from keras import regularizers

# Set the regularization strength
l2 = 0.001

# Create the model with L2 regularization
model = keras.Sequential([
    layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    
    layers.Conv2D(32, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.2),

    layers.Conv2D(64, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.3),

    layers.Conv2D(128, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.Conv2D(128, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.4),

    layers.Flatten(),
    layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
])

model.summary()

from tensorflow.keras import optimizers

model.compile(optimizer=optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

num_epochs = 40
# Train the model
history = model.fit(train_ds, 
                    validation_data=val_ds, 
                    epochs=num_epochs)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(num_epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.rcParams['text.color'] = 'black'
plt.tick_params(axis='x', colors='black')
plt.tick_params(axis='y', colors='black')
plt.show()

# set parameter values for increase accuracy and decrease loss value

data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal",
                           input_shape=(img_height, img_width, 3)),
        layers.RandomRotation(0.3),  # increased rotation angle
        layers.RandomZoom(0.3),  # increased zoom range
        layers.RandomContrast(0.3),  # added contrast adjustment
        layers.RandomBrightness(0.3),  # added brightness adjustment
    ]
)

from tensorflow.keras import layers

model = Sequential([
    data_augmentation,
    layers.Rescaling(1./255),
    
    layers.Conv2D(32, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.2),

    layers.Conv2D(64, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.3),

    layers.Conv2D(128, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.Conv2D(128, (3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.4),

    layers.Flatten(),
    layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(l2)),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'])

model.summary()

from tensorflow.keras import optimizers

model.compile(optimizer=optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

epochs = 30
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.rcParams['text.color'] = 'black'
plt.tick_params(axis='x', colors='black')
plt.tick_params(axis='y', colors='black')

plt.legend(loc='upper right')
plt.title('Training and Validation Loss')

plt.show()

import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

validation_dir = "/content/Plants_2/valid/"
img_height = 224
img_width = 224

# Get list of class names based on subdirectories
class_names = sorted(os.listdir(validation_dir))

# Load image using keras.preprocessing and predict with the model
for class_name in class_names:
    class_dir = os.path.join(validation_dir, class_name)
    for img_name in os.listdir(class_dir):
        img_path = os.path.join(class_dir, img_name)
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=(img_height, img_width))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        pred_class = class_names[np.argmax(score)]
        
        # Show image and predicted label
        plt.imshow(img)
        plt.title("Predicted Class: {}".format(pred_class))
        plt.axis('off')
        plt.rcParams['text.color'] = 'white'
        plt.tick_params(axis='x', colors='white')
        plt.tick_params(axis='y', colors='white')

        plt.show()

