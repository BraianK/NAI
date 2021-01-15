import numpy as np
from sklearn import svm

"""
Ładowanie danych z pliku tekstowego z odzieleniem po przecinku
"""
input_file = 'data_sonar.txt'
data = np.loadtxt(input_file, delimiter=',')
"""
Przypisanie do zmiennych kolumn z danymi i kolumn z wynikami
"""
X, y = data[:, :60], data[:, -1]
"""
Zasilenie danymi testowymi funkcjonalności SVM

"""
svc = svm.SVC(kernel='linear', C=1, gamma=100).fit(X, y)

XX = []
"""
Generowanie losowych danych do predykcji

"""
for i in range(60):
    tmp_min, tmp_max = X[:, i].min(), X[:, i].max()
    XX.append(np.arange(tmp_min, tmp_max, (tmp_max-tmp_min)/101)[:100])

XX = np.asarray(XX, dtype=np.float32)
"""
Generowanie predykcji
"""
Z = svc.predict(np.c_[XX.transpose()])
print(Z)