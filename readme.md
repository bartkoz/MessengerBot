# Super simple messenger bot with Watson AI
This has been created as a solution for recruitment task. It involves IBM's Watson to recognize mood of message and based on that either makes bot more sad or happy depending on a mood of received message. Additionally includes special command "mood" to check whether bot's mood is currently sad, happy or neutral.

What is needed:

```
pip install watson-developer-cloud
pip install fbchat
pip install python-decouple
```
All confidential data is hidden under python-decouple. Variables are:
+ FB_USER
+ FB_PASSWORD
+ WATSON_USER
+ WATSON_PASSWORD

To turn bot on:
```python fb-bot.py```
