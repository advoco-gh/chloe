# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
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

from typing import Text, List, Any, Dict, Optional


from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from rasa_sdk.events import FollowupAction, ActionExecuted

from rasa_sdk import Action, Tracker



class Validate_already_have_agent(FormValidationAction):
    def name(self) -> Text:
        return "validate_already_have_agent"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
        if not tracker.get_slot("want_to_continue"):
            slots_mapped_in_domain.append("goodbye")

        return slots_mapped_in_domain


class Validate_objection_already_have_PA_plan(FormValidationAction):
    def name(self) -> Text:
        return "validate_objection_already_have_PA_plan"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
            if tracker.get_slot("alternative_plan"):
                return slots_mapped_in_domain
            
            else:
                slots_mapped_in_domain.append("goodbye")
                return slots_mapped_in_domain





class action_chloe(Action):

    def name(self) -> Text:
        return "action_chloe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        a = tracker.events

        only_actions = []
        only_intents = []

        for x in a:
            if x['event'] == 'user':
                only_intents.append(x['parse_data']['intent']['name'])
            elif x['event'] == 'bot':
                try:
                    only_actions.append(x['metadata']['utter_action'])
                except:
                    pass

        if only_intents[-1] == "speak_twice":
            reply = only_actions[-1] 

        dispatcher.utter_message(response = reply)
        return []


