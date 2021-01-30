"""
Celem zadania jest nauczyć program rozpoznawania zadowolenia ludzi poprzez siec neuronowa na podstawie dostarczonych danych

## Autorzy
-Paweł Szyszkowski s18184
-Braian Kreft s16723

## Instalacja

pip install -r requirements.txt

## Uruchomienie
python happy.py

## Instrukcja użycia
Po uruchomieniu programu zostaną nam przewidywane wyniki
"""
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm

kr = tf.keras
"""
SVM dla klasyfikacji
Program, który za pomocą SVM klasyfikuje dane
"""
input_file = 'data_happy.txt'
data = np.loadtxt(input_file, delimiter=',')
X, y = data[:, 1:], data[:, 0]
svc = svm.SVC(kernel='linear', C=1, gamma=100).fit(X, y)
XX = data[-15:, 1:]
XX = np.asarray(XX)
YY = data[-15:, 0]
YY = np.asarray(YY)
Z = svc.predict(np.c_[XX])
good = 0
all = 0
for i in range(14):
    all = all + 1
    if Z[i] == YY[i]:
        good = good + 1

"""
Import danych do nuaki i testów z pliku CSV
"""
iris_data = pd.read_csv('data_happy2.csv')
class_names = ["Negative", "Positive"]
all_inputs = iris_data[['city_services', 'cost_housing', 'public_schools', 'trust_police', 'maintenance_streets',
                        'social_community']].values
all_types = iris_data['decision'].values
outputs_vals, outputs_ints = np.unique(all_types, return_inverse=True)
outputs_cats = kr.utils.to_categorical(outputs_ints)
inds = np.random.permutation(len(all_inputs))
train_inds, test_inds = np.array_split(inds, 2)
inputs_train, outputs_train = all_inputs[inds], outputs_cats[inds]
inputs_test,  outputs_test  = all_inputs[test_inds],  outputs_cats[test_inds]

"""
Definiowane modelu do nauki
"""
model = kr.models.Sequential()
model.add(kr.layers.Dense(500, input_shape=(6,)))
model.add(kr.layers.Activation("sigmoid"))
model.add(kr.layers.Dense(2))
model.add(kr.layers.Activation("softmax"))

"""
Kompilacja i optymalizacja modelu
"""
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

"""
Wytrenowanie modelu
"""
model.fit(inputs_train, outputs_train, epochs=1000, batch_size=1, verbose=1)

"""
Weryfikacja danych testowych
"""
loss, accuracy = model.evaluate(inputs_test, outputs_test, verbose=2)
print("Accuracy SVM: ", good / all)
print("\n\nLoss: %10.5f\tAccuracy: %2.2f %%" % (loss, accuracy * 100))

"""
Predykcja danych testowych
"""
prediction = np.around(model.predict(np.expand_dims(inputs_test[5], axis=0))).astype(np.int)[0]
probability_model = tf.keras.Sequential([model,
                                         tf.keras.layers.Softmax()])
predictions = probability_model.predict(inputs_test)

"""
Generowanie wykresu
"""


def plot_value_array(i, predictions_array, true_label, img):
    true_label, img = int(true_label[i][0]), img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(2), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'
    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                         100 * np.max(predictions_array),
                                         class_names[true_label]), color=color)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


num_rows = 5
num_cols = 3
num_images = num_rows * num_cols
plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
for i in range(num_images):
    plt.subplot(num_rows, num_cols, i + 1)
    plot_value_array(i, predictions[i], outputs_test, inputs_test)
plt.tight_layout()
plt.show()
