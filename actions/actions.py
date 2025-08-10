# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import random

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras import models

def switch(lang):
    msg = ''
    if lang == 0:
        msg = GetExerciseVideos()
    elif lang == 1:
        msg = 'The pursed lip breathing might help you with better emotional responses! (https://www.youtube.com/watch?v=7kpJ0QlRss4)'
    elif lang == 2:
        msg = 'Maybe try drinking tea, coffee, or a hot chocolate?'
    elif lang == 3:
        msg = GetComedyFilms()
    return msg

def GetExerciseVideos():
    URLs = ['https://www.youtube.com/watch?v=vFai116E69M',
            'https://www.youtube.com/watch?v=uep2HH5MW7k',
            'https://www.youtube.com/watch?v=WdbzQt_eLtc',
            'https://www.youtube.com/watch?v=Aj6jyIEmZzs&t=53']

    rnd = random.randint(0, len(URLs) - 1)
    link = URLs[rnd]

    messages = ['Here is a simple workout you can do! (' + link + ')',
                'Here is a simple workout you can try! (' + link + ')',
                'Here is a simple workout to help you! (' + link + ')',
                'Try this simple workout! (' + link + ')']

    rnd = random.randint(0, len(messages) - 1)
    msg = messages[rnd]
    return msg

def GetComedyFilms():
    films = ['Get Smart (2008)', 'Mean girls (2004)', 'Last Vegas (2013)',
             'Legally Blonde (2001)', 'Clueless (1995)', 'White Chicks (2004)',
             'Home Alone (1990)', 'Are We There Yet? (2005)', '21 Jump Steet (2012)']

    stream_pf = ['Google Play, Apple TV, and Amazon Prime',
                 'Paramount Plus, YouTube Primetime, and Amazon Prime',
                 'Google Play and Amazon Prime', 'ITVX and Amazon Prime',
                 'Paramount Plus, YouTube Primetime and Amazon Prime',
                 'Netflix, Amazon Prime and NOW', 'Disney Plus',
                 'Google Play', 'ITVX and Amazon Prime']

    rnd = random.randint(0, len(films) - 1)

    film = films[rnd]
    stream = stream_pf[rnd]

    msg = 'I think you would really like the movie "' + film + '", on ' + stream + '!'
    return msg

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

class ActionAnalyzeSentiments(Action):

    def name(self) -> Text:
        return "action_analyze_sentiment"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sentence = tracker.latest_message.get('text')
        pred_labels = sentimentAnalysis(sentence)
        for i in range(len(sentence)):
            print(sentence[i])
            if pred_labels[i] == 1:
                sentiment_label = 'pos'
            else:
                sentiment_label = 'neg'

        #dispatcher.utter_message(text=sentiment_label)

        return [SlotSet("sentiment", sentiment_label)]

class ActionSuggestRemedies(Action):

    def name(self) -> Text:
        return "action_suggest_remedies"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        rnd = random.randint(0, 3)
        msg = switch(rnd)

        dispatcher.utter_message(text=msg)

        return []

class ActionSuggestExercises(Action):

    def name(self) -> Text:
        return "action_suggest_exercises"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        msg = GetExerciseVideos()

        dispatcher.utter_message(text=msg)

        return []


class ActionSuggestFilms(Action):

    def name(self) -> Text:
        return "action_suggest_films"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        msg = GetComedyFilms()

        dispatcher.utter_message(text=msg)

        return []


class ActionSaveOption(Action):

    def name(self) -> Text:
        return "action_save_option"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        msg = tracker.latest_message.get('text')
        if '1' in msg:
            option = '1'
        elif '2' in msg:
            option = '2'
        elif '3' in msg:
            option = '3'

            #action_suggest_remedies
            rnd = random.randint(0, 3)
            msg = switch(rnd)
            msg = msg + "\nDid that help you?"

            dispatcher.utter_message(text=msg)
        else:
            option = 'unrec'

        #dispatcher.utter_message(text=option)

        return [SlotSet("option", option)]

class ActionResetSentiment(Action):

    def name(self) -> Text:
        return "action_reset_sentiment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("sentiment", None)]

class ActionResetOption(Action):

    def name(self) -> Text:
        return "action_reset_option"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("option", None)]