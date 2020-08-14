
from data_n_gen import data_prep, get_names
import data_n_gen

data_n_gen.data_prep()


from keras.layers import SimpleRNN, Dense, TimeDistributed
from keras.models import Sequential

model = Sequential()

# Add SimpleRNN layer of 50 units
model.add(SimpleRNN(50, input_shape=(data_n_gen.max_len+1, len(data_n_gen.vocab)), return_sequences=True))

# Add a TimeDistributed Dense layer of size same as the vocabulary
model.add(TimeDistributed(Dense(len(data_n_gen.vocab), activation='softmax')))

# Compile the model
model.compile(loss="categorical_crossentropy", optimizer="adam")

# Print the model summary
model.summary()

# Fit the model for 300 epochs using a batch size of 128 
model.fit(data_n_gen.input_data, data_n_gen.target_data, batch_size=128, epochs=300)


elvish_names = get_names(model, 10)
print(elvish_names)

from keras.models import save_model

save_model(model,"rnn_trained_on_all_data")
