# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

import json
import requests

from http import HTTPStatus

from typing import Any, Text, Dict, List, Union, Optional

from rasa.constants import DEFAULT_CREDENTIALS_PATH
from rasa.utils.io import read_config_file

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted, SlotSet
from rasa_sdk.executor import CollectingDispatcher

credentials_file = DEFAULT_CREDENTIALS_PATH
all_credentials = read_config_file(credentials_file)
restdb_credentials = all_credentials.get('restdb')
database = restdb_credentials['database']
collection = restdb_credentials['collection']

headers = {
    "content-type": "application/json",
    "x-apikey": restdb_credentials['apikey'],
    "cache-control": "no-cache",
}

"""Revertible mapped actions for explanations"""
class ActionExplainOxygen(Action):
    def name(self):
        return "action_explain_oxygen"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_oxygen_explanation")
        return [UserUtteranceReverted()]

class ActionExplainConcentrator(Action):
    def name(self):
        return "action_explain_concentrator"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_concentrator_explanation")
        return [UserUtteranceReverted()]

class ActionExplainTank(Action):
    def name(self):
        return "action_explain_tank"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_tank_explanation")
        return [UserUtteranceReverted()]

class ActionExplainWhy(Action):
    def name(self):
        return "action_explain_why"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_why_explanation")

class ActionExplainDifference(Action):
    def name(self):
        return "action_explain_difference"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_tank_explanation")
        dispatcher.utter_message(template="utter_concentrator_explanation")
        return [UserUtteranceReverted()]

class ActionExplainSize(Action):
    def name(self):
        return "action_explain_size"

    def run(self, dispatcher, tracker, domain):
        oxygen_kind = tracker.get_slot('oxygen_kind')
        if oxygen_kind == 'cylinder':
            explanation = 'utter_cylinder_size_explanation'
        else:
            explanation = 'utter_concentrator_size_explanation'
        dispatcher.utter_message(template=explanation)
        return [UserUtteranceReverted()]

class ActionLookup(Action):
    def name(self):
        return "action_lookup"

    def run(self, dispatcher, tracker, domain):
        url = 'https://{}.restdb.io/rest/{}'.format(database, collection)
        oxygen_size = tracker.get_slot('oxygen_size')
        oxygen_kind = tracker.get_slot('oxygen_kind')
        partno = tracker.get_slot('partno')
        if oxygen_size:
            q = {'description' : oxygen_size}
        elif oxygen_kind:
            q = {'description' : oxygen_kind }
        elif partno:
            q = {'partno', partno}
        result = requests.get(url, data={'q': json.dumps(q)}, headers=headers)
        if result.status_code == HTTPStatus.OK:
            return [Slotset(result.text)]
        else:
            print('{}: {}'.format(result.status_code, result.reason))
            return []

class OxygenForm(FormAction):
    def name(self):
        return "oxygen_form"

    @staticmethod
    def required_slots(tracker):
        return ["oxygen_kind", "oxygen_size"]

    def getfromtext(self, lookup):
        latest = self.from_text()
        print("getfromtext({})".format(latest))
        match = [term for term in lookup if (term in latest)]
        print('match {}'.format(match))
        return match

    def slot_mappings(self):
        return {
            "oxygen_kind": [
                self.from_entity(entity="oxygen_kind"),
                self.from_entity(entity="kind"),
                self.from_entity(entity="size_kind"),
            ],
            "oxygen_size": [
                self.from_entity(entity="oxygen_size"),
                self.from_entity(entity="size"),
                self.from_entity(entity="size_kind"),
            ],
        }

    @staticmethod
    def kind_db():
        return [
            "tank",
            "tanks",
            "bottle",
            "bottles",
            "cylinder",
            "cylinders",
            "container",
            "containers",
            "concentrator",
        ]

    @staticmethod
    def size_db():
        return [
            "small",
            "smaller",
            "little",
            "large",
            "larger",
            "big",
            "bigger",
            "portable",
            "stationary",
            "fixed",
            "ml6",
            "m6",
            "m9",
            "b",
            "c",
            "d",
            "e",
        ]

    @staticmethod
    def mapping_db():
        return {
            "tank" : "cylinder",
            "tanks" : "cylinder",
            "bottle" : "cylinder",
            "bottles" : "cylinder",
            "cylinders" : "cylinder",
            "container" : "cylinder",
            "containers" : "cylinder",
            "large" : "stationary",
            "larger" : "stationary",
            "big" : "stationary",
            "bigger" : "stationary",
            "fixed" : "stationary",
            "small" : "portable",
            "smaller" : "portable",
            "little" : "portable",
            "ml6" : "ML6",
            "b" : "B/M6",
            "m6" : "B/M6",
            "c" : "C/M9",
            "m9" : "C/M9",
            "d" : "D",
            "e" : "E",
        }

    def validate_kind(self, value, dispatcher, tracker, domain):
        lterm = value.lower()
        if lterm in self.kind_db():
            if lterm in self.mapping_db():
                lterm = self.mapping_db()[lterm]
            return {"oxygen_kind": lterm}
        else:
            dispatcher.utter_message(template="utter_wrong_kind")
            return {"oxygen_kind": None}

    def validate_size(self, value, dispatcher, tracker, domain):
        print("validate_size()")
        lterm = value.lower()
        if lterm in self.size_db():
            if lterm in self.mapping_db():
                lterm = self.mapping_db()[lterm]
            return {"oxygen_size": lterm}
        else:
            dispatcher.utter_message(template="utter_wrong_size")
            return {"oxygen_size": None}

    def getvalue(self, tracker, key):
        values = tracker.get_slot(key)
        if values:
            return values[0]

    def submit(self, dispatcher, tracker, domain):
        dispatcher.utter_message(template="utter_submit")
        url = 'https://{}.restdb.io/rest/{}'.format(database, collection)
        print(url)
        oxygen_size = self.getvalue(tracker, 'oxygen_size')
        oxygen_kind = self.getvalue(tracker, 'oxygen_kind')
        partno = self.getvalue(tracker, 'partno')
        if oxygen_size:
            q = {'size' : oxygen_size}
        elif oxygen_kind:
            q = {'type' : oxygen_kind}
        elif partno:
            q = {'partno': partno}
        print("query: {}".format(q))
        response = requests.get(url, params={'q': json.dumps(q)}, headers=headers)
        results = []

        if response.status_code == HTTPStatus.OK:
            print(response.text)
            data = json.loads(response.text)
            if data:
                for key, value in data[0].items():
                    ss = SlotSet(key, value)
                    print(ss)
                    results.append(ss)
        else:
            print('{}: {}'.format(response.status_code, response.reason))
        return results
