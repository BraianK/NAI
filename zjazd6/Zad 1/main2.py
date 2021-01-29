import pandas as pd
import numpy as np
import tensorflow as tf
kr = tf.keras


iris_data = pd.read_csv('data_happy.csv')
all_inputs = iris_data[['city_services', 'cost_housing', 'public_schools', 'trust_police', 'maintenance_streets', 'social_community']].values
all_types = iris_data['decision'].values
outputs_vals, outputs_ints = np.unique(all_types, return_inverse=True)
outputs_cats = kr.utils.to_categorical(outputs_ints)
inds = np.random.permutation(len(all_inputs))
train_inds, test_inds = np.array_split(inds, 2)
inputs_train, outputs_train = all_inputs[inds], outputs_cats[inds]
inputs_test,  outputs_test  = all_inputs[test_inds],  outputs_cats[test_inds]

model = kr.models.Sequential()
model.add(kr.layers.Dense(500, input_shape=(6,)))
model.add(kr.layers.Activation("sigmoid"))
model.add(kr.layers.Dense(2))
model.add(kr.layers.Activation("softmax"))

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

model.fit(inputs_train, outputs_train, epochs=10000, batch_size=1, verbose=1)

loss, accuracy = model.evaluate(inputs_test, outputs_test, verbose=1)

print("\n\nLoss: %10.5f\tAccuracy: %2.2f %%" % (loss, accuracy*100))

prediction = np.around(model.predict(np.expand_dims(inputs_test[57], axis=0))).astype(np.int)[0]
print("Model prediction in hot vector output: %s" % prediction)
print("Model prediction in actual Iris type: %s" % outputs_vals[prediction.astype(np.bool)][0])
print("Actual Iris flower type in data set: Vector: %s Type: %s" % (outputs_test[57].astype(np.int), outputs_vals[prediction.astype(np.bool)][0]))
