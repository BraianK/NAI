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

# Auto-membership function population is possible with .automf(3, 5, or 7)
income.automf(5)
bik_scoring.automf(3)
dependents.automf(3)
income.view()
dependents.view()
# Custom membership functions can be built interactively with a familiar,
# Pythonic API
scoring['not_allowed'] = fuzz.trimf(scoring.universe, [0, 0, 0])
scoring['very_low'] = fuzz.trimf(scoring.universe, [0, 0, 60000])
scoring['low'] = fuzz.trimf(scoring.universe, [40000, 60000, 100000])
scoring['medium'] = fuzz.trimf(scoring.universe, [80000, 150000, 190000])
scoring['high'] = fuzz.trimf(scoring.universe, [120000, 200000, 250000])
scoring['very_high'] = fuzz.trimf(scoring.universe, [200000, 250000, 250000])
# Income poor
rule1 = ctrl.Rule(income['poor'] & bik_scoring['good'] & dependents['good'], scoring['low'])
rule2 = ctrl.Rule(income['poor'] & bik_scoring['good'] & dependents['average'], scoring['very_low'])
rule3 = ctrl.Rule(income['poor'] & bik_scoring['good'] & dependents['poor'], scoring['very_low'])
rule4 = ctrl.Rule(income['poor'] & bik_scoring['average'] & dependents['poor'], scoring['not_allowed'])
rule5 = ctrl.Rule(income['poor'] & bik_scoring['average'] & dependents['average'], scoring['not_allowed'])
rule6 = ctrl.Rule(income['poor'] & bik_scoring['average'] & dependents['good'], scoring['very_low'])
rule7 = ctrl.Rule(income['poor'] & bik_scoring['poor'] & dependents['good'], scoring['not_allowed'])
rule8 = ctrl.Rule(income['poor'] & bik_scoring['poor'] & dependents['average'], scoring['not_allowed'])
rule9 = ctrl.Rule(income['poor'] & bik_scoring['poor'] & dependents['poor'], scoring['not_allowed'])
# Income mediocre
rule10 = ctrl.Rule(income['mediocre'] & bik_scoring['good'] & dependents['good'], scoring['medium'])
rule11 = ctrl.Rule(income['mediocre'] & bik_scoring['good'] & dependents['average'], scoring['medium'])
rule12 = ctrl.Rule(income['mediocre'] & bik_scoring['good'] & dependents['poor'], scoring['low'])
rule13 = ctrl.Rule(income['mediocre'] & bik_scoring['average'] & dependents['poor'], scoring['very_low'])
rule14 = ctrl.Rule(income['mediocre'] & bik_scoring['average'] & dependents['average'], scoring['very_low'])
rule15 = ctrl.Rule(income['mediocre'] & bik_scoring['average'] & dependents['good'], scoring['low'])
rule16 = ctrl.Rule(income['mediocre'] & bik_scoring['poor'] & dependents['good'], scoring['not_allowed'])
rule17 = ctrl.Rule(income['mediocre'] & bik_scoring['poor'] & dependents['average'], scoring['not_allowed'])
rule18 = ctrl.Rule(income['mediocre'] & bik_scoring['poor'] & dependents['poor'], scoring['not_allowed'])
# Income average
rule19 = ctrl.Rule(income['average'] & bik_scoring['good'] & dependents['good'], scoring['high'])
rule20 = ctrl.Rule(income['average'] & bik_scoring['good'] & dependents['average'], scoring['high'])
rule21 = ctrl.Rule(income['average'] & bik_scoring['good'] & dependents['poor'], scoring['medium'])
rule22 = ctrl.Rule(income['average'] & bik_scoring['average'] & dependents['poor'], scoring['very_low'])
rule23 = ctrl.Rule(income['average'] & bik_scoring['average'] & dependents['average'], scoring['very_low'])
rule24 = ctrl.Rule(income['average'] & bik_scoring['average'] & dependents['good'], scoring['low'])
rule25 = ctrl.Rule(income['average'] & bik_scoring['poor'] & dependents['good'], scoring['low'])
rule26 = ctrl.Rule(income['average'] & bik_scoring['poor'] & dependents['average'], scoring['very_low'])
rule27 = ctrl.Rule(income['average'] & bik_scoring['poor'] & dependents['poor'], scoring['not_allowed'])
# Income decent
rule28 = ctrl.Rule(income['decent'] & bik_scoring['good'] & dependents['good'], scoring['very_high'])
rule29 = ctrl.Rule(income['decent'] & bik_scoring['good'] & dependents['average'], scoring['high'])
rule30 = ctrl.Rule(income['decent'] & bik_scoring['good'] & dependents['poor'], scoring['medium'])
rule31 = ctrl.Rule(income['decent'] & bik_scoring['average'] & dependents['poor'], scoring['low'])
rule32 = ctrl.Rule(income['decent'] & bik_scoring['average'] & dependents['average'], scoring['medium'])
rule33 = ctrl.Rule(income['decent'] & bik_scoring['average'] & dependents['good'], scoring['medium'])
rule34 = ctrl.Rule(income['decent'] & bik_scoring['poor'] & dependents['good'], scoring['low'])
rule35 = ctrl.Rule(income['decent'] & bik_scoring['poor'] & dependents['average'], scoring['very_low'])
rule36 = ctrl.Rule(income['decent'] & bik_scoring['poor'] & dependents['poor'], scoring['not_allowed'])
# Income good
rule37 = ctrl.Rule(income['good'] & bik_scoring['good'] & dependents['good'], scoring['very_high'])
rule38 = ctrl.Rule(income['good'] & bik_scoring['good'] & dependents['average'], scoring['very_high'])
rule39 = ctrl.Rule(income['good'] & bik_scoring['good'] & dependents['poor'], scoring['high'])
rule40 = ctrl.Rule(income['good'] & bik_scoring['average'] & dependents['poor'], scoring['medium'])
rule41 = ctrl.Rule(income['good'] & bik_scoring['average'] & dependents['average'], scoring['high'])
rule42 = ctrl.Rule(income['good'] & bik_scoring['average'] & dependents['good'], scoring['high'])
rule43 = ctrl.Rule(income['good'] & bik_scoring['poor'] & dependents['good'], scoring['medium'])
rule44 = ctrl.Rule(income['good'] & bik_scoring['poor'] & dependents['average'], scoring['low'])
rule45 = ctrl.Rule(income['good'] & bik_scoring['poor'] & dependents['poor'], scoring['not_allowed'])

amount_ctrl = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15,
     rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29,
     rule30, rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40, rule41, rule42, rule43,
     rule44, rule45])
amount = ctrl.ControlSystemSimulation(amount_ctrl)
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
    print(amount.output['scoring'])
else:
    print(amount.output['scoring'])
scoring.view(sim=amount)
