# sentiment analysis

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras import models

def sentimentAnalysis(text):
    # load existing model
    model = models.load_model('LSTM_tf_epoch2.h5')
    #model.summary()

    # tokenization
    tokenizer = Tokenizer(num_words=2000, oov_token='')
    tokenizer.fit_on_texts(text)
    # convert to a sequence
    sequences = tokenizer.texts_to_sequences(text)
    # pad the sequence
    sequences_matrix = sequence.pad_sequences(sequences, maxlen=140)
    # Get labels based on probability 1 if p>= 0.5 else 0
    prediction = model.predict(sequences_matrix)
    pred_labels = []
    for i in prediction:
        if i >= 0.51:
            pred_labels.append(1)
        else:
            pred_labels.append(0)
    return pred_labels

try:
    while True:
        text = input("Jot down your thoughts: ")
        sentence = [text]
        pred_labels = sentimentAnalysis(sentence)
        for i in range(len(sentence)):
            print(sentence[i])
            if pred_labels[i] == 1:
                s = 'pos'
            else:
                s = 'neg'
            print("Predicted sentiment : ", s)
except KeyboardInterrupt:
    pass