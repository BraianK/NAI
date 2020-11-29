import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
income = ctrl.Antecedent(np.arange(0, 20001, 100), 'income')
expenses = ctrl.Antecedent(np.arange(0, 20001, 100)  , 'expenses')
bik_scoring = ctrl.Antecedent(np.arange(0, 11, 1) , 'bik_scoring')
dependents = ctrl.Antecedent(np.arange(0, 9, 1) , 'dependents')
scoring = ctrl.Consequent(np.arange(0, 250000, 1000), 'scoring')

# Auto-membership function population is possible with .automf(3, 5, or 7)
income.automf(3)
expenses.automf(3)
bik_scoring.automf(3)
dependents.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
scoring['low'] = fuzz.trimf(scoring.universe, [0, 0, 120000])
scoring['medium'] = fuzz.trimf(scoring.universe, [0, 120000, 250000])
scoring['high'] = fuzz.trimf(scoring.universe, [120000, 250000, 250000])

# You can see how these look with .view()
expenses['average'].view()

rule1 = ctrl.Rule(income['poor'] & expenses['good'] & bik_scoring['good'] & dependents['good'], scoring['low'])
rule2 = ctrl.Rule(income['average'] | expenses['average'], scoring['medium'])
rule3 = ctrl.Rule(income['good'] & expenses['poor'] & bik_scoring['poor'], scoring['high'])

rule1.view()

amount_ctrl = ctrl.ControlSystem([rule1,rule2,rule3])
amount = ctrl.ControlSystemSimulation(amount_ctrl)
amount.input['income'] = 20000
amount.input['expenses'] = 19000
amount.input['bik_scoring'] = 0
amount.input['dependents'] = 0

# Crunch the numbers
amount.compute()
print(amount.output['scoring'])
scoring.view(sim=amount)