"""
Celem zadania jest nauczyć program rozpoznawania zwierząt poprzez siec neuronowa.

## Autorzy
-Paweł Szyszkowski s18184
-Braian Kreft s16723

## Instalacja

pip install -r requirements.txt

## Uruchomienie
python animals.py

## Instrukcja użycia
Po uruchomieniu programu zostaną nam przewidywane wyniki
"""
import tensorflow as tf
import numpy as np
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

"""
Import danych do nuaki i testów z biblioteki tensorflow
"""
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0

for i in range(train_labels.shape[0]):
    x = train_labels[i]
    train_labels[i] = x if x < 2 else (2 if x < 8 else (3 if x == 8 else 4))
for i in range(test_labels.shape[0]):
    x = test_labels[i]
    test_labels[i] = x if x < 2 else (2 if x < 8 else (3 if x == 8 else 4))

class_names = ['airplane', 'automobile', 'animal', 'ship', 'truck']
"""
Definiowane modelu do nauki
"""
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.summary()
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(5))
model.summary()

"""
Kompilacja i optymalizacja modelu
"""
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
"""
Wytrenowanie modelu
"""
history = model.fit(train_images, train_labels, epochs=10,
                    validation_data=(test_images, test_labels))
"""
Predykcja danych testowych
"""
probability_model = tf.keras.Sequential([model,
                                         tf.keras.layers.Softmax()])
predictions = probability_model.predict(test_images)

"""
Generowanie wykresu
"""


def plot_image(i, predictions_array, true_label, img):
    true_label, img = true_label[i][0], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'
    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                         100 * np.max(predictions_array),
                                         class_names[true_label]),
               color=color)


def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i][0]
    plt.grid(False)
    plt.xticks(range(5))
    plt.yticks([])
    thisplot = plt.bar(range(5), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


num_rows = 5
num_cols = 3
num_images = num_rows * num_cols
plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(num_rows, 2 * num_cols, 2 * i + 2)
    plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()

test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print(test_acc)
