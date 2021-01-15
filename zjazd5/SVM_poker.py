"""
SVM dla klasyfikacji
Program, który za pomocą SVM klasyfikuje dane

## Autorzy
-Paweł Szyszkowski s18184
-Braian Kreft s16723

## Instalacja

pip install -r requirements.txt

## Uruchomienie
python SVM_poker.py

## Instrukcja użycia
Po uruchomieniu programu zostaną nam przewidywane wyniki
"""

import numpy as np
from sklearn import svm
from numpy import random

"""
Ładowanie danych z pliku tekstowego z odzieleniem po przecinku
"""

input_file = 'data_poker.txt'
data = np.loadtxt(input_file, delimiter=',')
"""
Przypisanie do zmiennych kolumn z danymi i kolumn z wynikami
"""
X, y = data[:, :10], data[:, -1]
"""
Zasilenie danymi testowymi funkcjonalności SVM

"""
svc = svm.SVC(kernel='linear', C=1, gamma=100).fit(X, y)

XX = []
"""
Generowanie losowych danych do predykcji

"""
for i in range(10):
    if i % 2 == 0:
        min, max = 1, 5
    else:
        min, max = 1, 14
    XX.append(random.randint(min, max, size=200))

XX = np.asarray(XX, dtype=np.float32)
"""
Generowanie predykcji
"""
Z = svc.predict(np.c_[XX.transpose()])
print(Z)