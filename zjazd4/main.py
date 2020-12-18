"""
Rekomendator filmów
Program rekomnedujący filmy na podstawie danych zebranych w bazie

## Autorzy
-Paweł Szyszkowski s18184
-Braian Kreft s16723

## Instalacja

pip install -r requirements.txt

## Uruchomienie
python main.py

## Instrukcja użycia
Po uruchomieniu programu należy:
-wybrać użytkownika, któremu chcemy znaleźć rekomendacje
-wybrać algorytm, którego chcemy użyć
-po zaprezentowaniu wyników możemy wybrać opcję pobrania opisu do filmu

Działanie programu zaprezentowane jest w załączonym nagraniu.

"""
import json

import numpy as np
from imdb import IMDb

ia = IMDb()


def euclidean_score(dataset, user1, user2):
    """Metoda do wyliczania podbieństwa pomiędzy użytkownikami
    Parametry wejściowe:
        dataset (dict): Zaimportowane dane użytkowników
        user1 (str): Pierwszy użytkownik
        user2 (str): Drugi użytkownik

    Parametry wyjściowe:
        float: Stopień podobieństwa
    """
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    if len(common_movies) == 0:
        return 0

    squared_diff = []

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))

    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


def pearson_score(dataset, user1, user2):
    """Metoda do wyliczania podbieństwa pomiędzy użytkownikami
    Parametry wejściowe:
        dataset (dict): zaimportowane dane użytkowników
        user1 (str): Pierwszy użytkownik
        user2 (str): Drugi użytkownik

    Parametry wyjściowe:
            float: Stopień podobieństwa
    """
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    num_ratings = len(common_movies)

    if num_ratings == 0:
        return 0

    user1_sum = np.sum([dataset[user1][item] for item in common_movies])
    user2_sum = np.sum([dataset[user2][item] for item in common_movies])

    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in common_movies])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in common_movies])

    sum_of_products = np.sum([dataset[user1][item] * dataset[user2][item] for item in common_movies])

    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)


def movie_description_get(title):
    """Metoda do pobierania i wyświetlania opisu filmu z IMDB

    Parametry wejściowe:
        title (str): Tytuł filmu
    """
    items = ia.search_movie(title)
    i = 0
    while i < len(items):
        print('\t[' + str(i) + '] ' + items[i]['title'] + (
            ' (' + str(items[i]['year']) + ')' if 'year' in items[i] else ''))
        i += 1

    movie_index = int(input('\nKtóry film masz na myśli? '))
    movie_details = ia.get_movie(items[movie_index].movieID)

    print(('\nOpis: ' + movie_details['plot'][0]) if 'plot' in movie_details else '\nBrak opisu')


def print_result(user_name, user_dict):
    """Metoda do wyświtlania najlepiej i najgorzej ocenionych filmów uzytkownika

    Parametry wejściowe:
        user_name (str): Użytkownik

    Parametry wyjściowe:
        array[int]: Lista wyświetlonych filmów
    """
    print('Na podstawie danych uzytkownika ' + user_name)
    movie_without_duplicates = {}
    for key, value in user_dict.items():
        if key not in data[user].keys():
            movie_without_duplicates[key] = value
    sorted_dict = dict(sorted(movie_without_duplicates.items(), key=lambda element: element[1], reverse=True))
    best7 = dict(list(sorted_dict.items())[:7])
    worse7 = dict(list(sorted_dict.items())[-7:])
    counter = 0
    movie_all = []

    print('\nPolecam filmy:')
    for itm in best7:
        print('\t[' + str(counter) + '] ' + itm + ' ' + str(best7[itm]))
        counter += 1
        movie_all.append(itm)

    print('\nNie polecam filmów:')
    for itm in worse7:
        print('\t[' + str(counter) + '] ' + itm + ' ' + str(worse7[itm]))
        counter += 1
        movie_all.append(itm)
    return movie_all


def select_user():
    """Metoda do wyświetlania listy użytkowników i wyboru jednego z nich

    Parametry wyjściowe:
        str: Wybrany użytkownik
    """
    counter = 0
    user_list = []
    print('\nWybierz użytkownika')
    for item in data:
        print('\t[' + str(counter) + '] ' + item)
        user_list.append(item)
        counter += 1
    return user_list[int(input())]


def select_score_type():
    """Metoda do wyświetlania możliwysz algorytmów i wyboru jednego z nich

    Parametry wyjściowe:
        str: Wybrany algorytm
    """
    counter = 0
    score_type_dict = ['Pearson', 'Euclidean']
    score_type_list = []
    print('Wybierz algorytm')
    for item in score_type_dict:
        print('\t[' + str(counter) + '] ' + item)
        score_type_list.append(item)
        counter += 1
    return score_type_list[int(input())]


if __name__ == '__main__':
    ratings_file = 'ratings.json'
    with open(ratings_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    user = select_user()
    score_type = select_score_type()
    show_description = True
    score_array = []

    for item in data:
        if item != user:
            if score_type == 'Euclidean':
                score_array.append({'score': euclidean_score(data, user, item), 'user': item})
            else:
                score_array.append({'score': pearson_score(data, user, item), 'user': item})

    max_score = max(score_array, key=lambda x: x['score'])

    user_movies = data[max_score['user']]
    movie_all_list = print_result(max_score['user'], user_movies)
    show_description = True if input('\n[tak/nie] Czy wyświetlić szczegóły jednego z filmów? ') == 'tak' else False
    while show_description:
        movie = int(input('\nW celu pobrania opisu filmu podaj numer zaprezentowany obok tytułu: '))
        movie_description_get(movie_all_list[movie])
        show_description = True if input('\n[tak/nie] Czy wyświetlić szczegóły innego filmu? ') == 'tak' else False
        if show_description:
            print_result(max_score['user'], user_movies)
