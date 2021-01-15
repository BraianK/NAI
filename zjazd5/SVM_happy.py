"""
SVM dla klasyfikacji
Program, który za pomocą SVM klasyfikuje dane

## Autorzy
-Paweł Szyszkowski s18184
-Braian Kreft s16723

## Instalacja

pip install -r requirements.txt

## Uruchomienie
python SVM_happy.py

## Instrukcja użycia
Po uruchomieniu programu zostaną nam przewidywane wyniki
"""
import numpy as np
from sklearn import svm
from numpy import random

"""
Ładowanie danych z pliku tekstowego z odzieleniem po przecinku
"""

input_file = 'data_happy.txt'
data = np.loadtxt(input_file, delimiter=',')

"""
Przypisanie do zmiennych kolumn z danymi i kolumn z wynikami
"""

X, y = data[:, 1:], data[:, 0]
"""
Zasilenie danymi testowymi funkcjonalności SVM

"""
svc = svm.SVC(kernel='linear', C=1, gamma=100).fit(X, y)

"""
Generowanie losowych danych do predykcji

"""
XX = random.randint(1,6, size=(100, 6))
XX = np.asarray(XX)

"""
Generowanie predykcji
"""
Z = svc.predict(np.c_[XX])

print(Z)
