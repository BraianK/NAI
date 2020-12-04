"""Wyliczanie zdolności kredytowej - wyliczanie odbywa się za pomocą czterech wartości
przychodów, wydatków, wartosci bik i ilości osób na utrzymaniu
Biorąc pod uwagę te parametry i zapisane reguły jesteśmy wstanie wyliczyć orientacyjną zdolność kredytową.

Twórcy:
Paweł Szyszkowski s18184, Braian Kreft s16723

Instrukcja użycia:
    Po uruchomieniu programu aplikacja prosi nas o podanie czterech wartości:
        salary (int) - miesięczne dochody 0 - 20000 zwiększajaca się o 100
        expenses (int) - miesięczne wydatki
        bik_scoring (int) - wartość bik 0-10 (im mniej tym lepiej)
        dependents (int) - ilość osób na utrzymaniu 0-10 (im mniej tym lepiej)
    Na podstwie wyżej wymienionych danych i reguł system wylicza nam zdolność.
    Reguły zostały przez nas spisane na podstawie własnych ustaleń i odczuć

"""
from collections import deque

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
income = ctrl.Antecedent(np.arange(0, 20001, 100), 'income')
bik_scoring = ctrl.Antecedent(np.arange(0, 11, 1), 'bik_scoring')
dependents = ctrl.Antecedent(np.arange(0, 9, 1), 'dependents')
scoring = ctrl.Consequent(np.arange(0, 250000, 1000), 'scoring')

"""Parametry wejściowe:
        income - 5 stopniowa skala wprowadzona na podstawie dochodów i wydatków
        bik_scoring - 3 stopniowa skala wprowadzana przez użytkownika
        dependents - 3 stopniowa skala wprowadzona przez użytkownika
"""

# Auto-membership function population is possible with .automf(3, 5, or 7)
income.automf(5)
bik_scoring.automf(3)
dependents.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
"""Przedziały zdolności kredytowej na podstawie przyjętej przez nas skali 0-250000
"""
scoring['not_allowed'] = fuzz.trimf(scoring.universe, [0, 0, 0])
scoring['very_low'] = fuzz.trimf(scoring.universe, [0, 0, 60000])
scoring['low'] = fuzz.trimf(scoring.universe, [40000, 60000, 100000])
scoring['medium'] = fuzz.trimf(scoring.universe, [80000, 150000, 190000])
scoring['high'] = fuzz.trimf(scoring.universe, [120000, 200000, 250000])
scoring['very_high'] = fuzz.trimf(scoring.universe, [200000, 250000, 250000])
"""Reguły, określone przez nas na podstawie przedziałów skali kredytowej i parametrów wejściowych
"""

rule1 = ctrl.Rule((income['decent'] | income['good'] | income['average']) & (bik_scoring['poor'] & dependents['poor']), scoring['not_allowed'])
rule2 = ctrl.Rule((income['poor'] | income['mediocre']) & bik_scoring['poor'], scoring['not_allowed'])
rule3 = ctrl.Rule((income['poor'] & bik_scoring['average']) & (dependents['average'] | dependents['poor']), scoring['not_allowed'])

rule4 = ctrl.Rule((income['poor'] & bik_scoring['good']) & (dependents['average'] | dependents['poor']), scoring['very_low'])
rule5 = ctrl.Rule((income['decent'] | income['average']) & (bik_scoring['poor'] & dependents['average']), scoring['very_low'])
rule6 = ctrl.Rule((income['average'] & bik_scoring['average']) & (dependents['poor'] | dependents['average']), scoring['very_low'])
rule7 = ctrl.Rule(income['poor'] & bik_scoring['average'] & dependents['good'], scoring['very_low'])
rule8 = ctrl.Rule((income['mediocre'] & bik_scoring['average']) & (dependents['average'] | dependents['poor']), scoring['very_low'])

rule9 = ctrl.Rule((income['average'] | income['mediocre']) & (bik_scoring['average'] & dependents['good']), scoring['low'])
rule10 = ctrl.Rule((income['decent'] | income['average']) & (bik_scoring['poor'] & dependents['good']), scoring['low'])
rule11 = ctrl.Rule((income['poor'] & bik_scoring['good']) & dependents['good'], scoring['low'])
rule12 = ctrl.Rule((income['mediocre'] & bik_scoring['good']) & dependents['poor'], scoring['low'])
rule13 = ctrl.Rule((income['good'] & bik_scoring['poor']) & dependents['average'], scoring['low'])
rule14 = ctrl.Rule(income['decent'] & bik_scoring['average'] & dependents['poor'], scoring['low'])

rule15 = ctrl.Rule((income['decent'] & bik_scoring['average']) & (dependents['average'] | dependents['good']), scoring['medium'])
rule16 = ctrl.Rule((income['mediocre'] & bik_scoring['good']) & (dependents['good'] | dependents['average']), scoring['medium'])
rule17 = ctrl.Rule((income['average'] | income['decent'])  & (bik_scoring['good'] & dependents['poor']), scoring['medium'])
rule18 = ctrl.Rule((income['good'] & bik_scoring['poor']) & dependents['good'], scoring['medium'])
rule19 = ctrl.Rule((income['good'] & bik_scoring['average']) & dependents['poor'], scoring['medium'])

rule20 = ctrl.Rule((income['average'] & bik_scoring['good']) & (dependents['good'] & dependents['average']), scoring['high'])
rule21 = ctrl.Rule((income['good'] & bik_scoring['average']) & (dependents['average'] & dependents['good']), scoring['high'])
rule22 = ctrl.Rule(income['decent'] & bik_scoring['good'] & dependents['average'], scoring['high'])
rule23 = ctrl.Rule(income['good'] & bik_scoring['good'] & dependents['poor'], scoring['high'])

rule24 = ctrl.Rule((income['good'] & bik_scoring['good']) & (dependents['good'] | dependents['average']), scoring['very_high'])
rule25 = ctrl.Rule(income['decent'] & bik_scoring['good'] & dependents['good'], scoring['very_high'])


amount_ctrl = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15,
     rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25])
amount = ctrl.ControlSystemSimulation(amount_ctrl)

"""Wprowadzanie danych wejściowych i proste instrukcje warunkowe"""
salary = int(input("Podaj wynagrodzenie\n"))
expenses = int(input("Podaj wydatki\n"))
if expenses >= salary:
    income = 0
else:
    income = salary - expenses
bik = int(input("Podaj wartosc bik 0-10\n"))
bik = 10 - bik
dependents = int(input("Podaj ilość osób na utrzymaniu 0-10\n"))
dependents = 10 - dependents
amount.input['income'] = income
amount.input['bik_scoring'] = int(bik)
amount.input['dependents'] = int(dependents)

# Crunch the numbers
amount.compute()
if amount.output['scoring'] < 2000:
    print("\n Nie masz zdolności kredytowej")
else:
    print("\n Twoja zdolność wynosi: " + str(amount.output['scoring']))
scoring.view(sim=amount)
