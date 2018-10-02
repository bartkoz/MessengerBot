from fbchat import Client
from fbchat.models import *
import random
import json
from watson_developer_cloud import ToneAnalyzerV3
from decouple import config


class MessengerBot(Client):
    global mood
    mood = 0

    def onMessage(self, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        # mark as read
        global mood
        self.markAsRead(author_id)
        # fetch received message
        msgText = message_object.text
        # check if mood command has been used
        if msgText == "mood":
            self.send(Message(text="Current mood is "+str(mood)), thread_id=thread_id,
                      thread_type=thread_type)
        else:
            # generic messages
            messages_sadness = ["I'm sad", "That's depressing", "Please, stop!",
                                "I cannot take it anymore", "Please don't depress me"]
            messages_joy = ["That's awesome!", "Hooray!",
                            "It's great!", "Cool!", "Good!"]
            messages_analytical = ["Hmmm...", "Okay.",
                                   "You're right.", "True that.", "Yep."]
            # Triggering watson
            tone_analyzer = ToneAnalyzerV3(
                version="2017-09-21",
                username=config("WATSON_USER"),
                password=config("WATSON_PASSWORD"),)

            tone_analysis = tone_analyzer.tone(
                {'text': msgText},
                'application/json').get_result()
            # read tone from received json
            try:
                tone = tone_analysis['document_tone']['tones'][0]['tone_name']
            except IndexError:
                tone = None
            # modify mood
            if tone is not None:
                if tone == "Sadness":
                    mood -= 1
                elif tone == "Joy":
                    mood += 1
            # assign proper response
            print(tone)
            if mood < 0:
                reply = random.choice(messages_sadness)
            elif mood > 0:
                reply = random.choice(messages_joy)
            elif mood == 0:
                reply = random.choice(messages_analytical)
            # check if author of msg isn't bot itself if not, send the message
            if author_id != self.uid:
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)
        # mark as delivered
        self.markAsDelivered(author_id, thread_id)


# setup
client = MessengerBot(config("FB_USER"), config("FB_PASSWORD"))

client.listen()
