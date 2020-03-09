# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

"""Revertible mapped actions for explanations"""
class ActionExplain(Action):
    def name(self):
        return "action_explain_oxygen"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_oxygen_explanation")
        return [UserUtteranceReverted()]

class ActionExplain(Action):
    def name(self):
        return "action_explain_concentrator"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_concentrator_explanation")
        return [UserUtteranceReverted()]

class ActionExplain(Action):
    def name(self):
        return "action_explain_tank"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_tank_explanation")
        return [UserUtteranceReverted()]

class ActionExplain(Action):
    def name(self):
        return "action_explain_why"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_why_explanation")
        return [UserUtteranceReverted()]
