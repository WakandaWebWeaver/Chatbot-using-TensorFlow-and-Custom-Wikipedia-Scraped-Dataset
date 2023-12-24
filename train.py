import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.callbacks import ModelCheckpoint


with open('data.txt', 'r', encoding='utf-8') as file:
    texts = file.readlines()

tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(texts)
total_words = len(tokenizer.word_index) + 1

input_sequences = []
for line in texts:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i + 1]
        input_sequences.append(n_gram_sequence)

max_sequence_length = max([len(x) for x in input_sequences])
input_sequences = tf.keras.preprocessing.sequence.pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')

X, y = input_sequences[:, :-1], input_sequences[:, -1]
y = tf.keras.utils.to_categorical(y, num_classes=total_words)

if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
    # Use GPU if available
    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        model = Sequential()
        model.add(Embedding(total_words, 50, input_length=max_sequence_length - 1))
        model.add(LSTM(100))
        model.add(Dense(total_words, activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # Add ModelCheckpoint callback
        checkpoint = ModelCheckpoint('model_checkpoint.h5', save_best_only=True)
        model.fit(X, y, epochs=20, batch_size=64, callbacks=[checkpoint], verbose=1)

else:
    print("GPU not found. Training on CPU.")
    # Use CPU
    model = Sequential()
    model.add(Embedding(total_words, 50, input_length=max_sequence_length - 1))
    model.add(LSTM(100))
    model.add(Dense(total_words, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    checkpoint = ModelCheckpoint('model_checkpoint.h5', save_best_only=True)
    model.fit(X, y, epochs=1, batch_size=64, verbose=1)

def generate_text(seed_text, next_words, model, max_sequence_length):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = tf.keras.preprocessing.sequence.pad_sequences([token_list], maxlen=max_sequence_length - 1, padding='pre')
        predicted_probs = model.predict(token_list, verbose=0)
        predicted = np.argmax(predicted_probs)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text

while True:
    seed_text = input("Say something: ")
    if seed_text.lower() != "quit":
        generated_text = generate_text(seed_text, next_words=5, model=model, max_sequence_length=max_sequence_length)
        print(generated_text)
    else:
        break
