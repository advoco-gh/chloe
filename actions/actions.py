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


class Validate_conversion_form(FormValidationAction):
    def name(self) -> Text:
        return "validate_conversion_form"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
        if not tracker.get_slot("app_call_time"):
            slots_mapped_in_domain.append("goodbye")

        if not tracker.get_slot("age_info"):
            slots_mapped_in_domain.append("goodbye")
        print('{}, slots: {}'.format(self.name(), slots_mapped_in_domain))
        return slots_mapped_in_domain


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
        print('{}, slots: {}'.format(self.name(), slots_mapped_in_domain))
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
            print('{}, slots: {}'.format(self.name(), slots_mapped_in_domain))

            return slots_mapped_in_domain


class action_trigger_conversion_form(Action):

    def name(self) -> Text:
        return "action_trigger_conversion_form"

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

        # if only_intents[-1] == "speak_twice":
        #     reply = only_actions[-1]
        if only_actions[-1] == 'utter_chloe_greeting':
            print('{}, intent: {}, action: {}, reply; {}'.format(
                self.name(), only_intents[-1], only_actions[-1], reply))

            dispatcher.utter_message(response='utter_chloe_greeting_repeat')
            return []

        else:
            rules = {'already_have_agent': 'already_have_agent',
                     'objection_already_have_PA_plan': 'objection_already_have_PA_plan',
                     'question_related_to_age': 'question_related_to_age'}
            reply_action = rules[only_intents[-1]]
            print('{}, intent: {}, action: {}, reply; {}'.format(
                self.name(), only_intents[-1], only_actions[-1], reply_action))

            return [FollowupAction(name=reply_action)]


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
        print('{}, intent: {}, action: {}, reply; {}'.format(
            self.name(), only_intents[-1], only_actions[-1], reply))

        dispatcher.utter_message(response=reply)
        return []


class action_rule_only_once(Action):

    def name(self) -> Text:
        return "action_rule_only_once"

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

        if only_actions[-1] == 'utter_chloe_greeting' and only_intents[-1] != 'question_related_to_numbers ':
            reply = 'utter_chloe_greeting_repeat'

        else:
            reply = ''
            for intent in ['fees_question', 'question_related_to_scam', 'question_related_to_numbers', 'not_singaporean', 'pa_plan_coverage']:
                if only_intents.count(intent) > 1:
                    reply = 'utter_chloe_goodbye'

            if reply != 'utter_chloe_goodbye':
                rules = {'fees_question':
                         'utter_chloe_pa_fees',
                         'question_related_to_scam':
                         'utter_chloe_scam',
                         'question_related_to_numbers':
                         'utter_chloe_number_info',
                         'not_singaporean':
                         'utter_chloe_not_local',
                         'pa_plan_coverage':
                         'utter_chloe_pa_coverage',
                         'manager_question':
                         'utter_chloe_manager_introduction',
                         'question_speak_chinese':
                         'utter_chloe_language_barrier',
                         'objection_i_am_agent':
                         'utter_chloe_goodbye',
                         'morning':
                         'utter_chloe_greeting_repeat',
                         'afternoon':
                         'utter_chloe_greeting_repeat',
                         'evening':
                         'utter_chloe_greeting_repeat',
                         'date_day':
                         'utter_chloe_greeting_repeat',
                         'age':
                         'utter_chloe_greeting_repeat',
                         }
                reply = rules[only_intents[-1]]

        print('{}, intent: {}, action: {}, reply; {}'.format(
            self.name(), only_intents[-1], only_actions[-1], reply))

        dispatcher.utter_message(response=reply)
        return []


class action_busy_reply(Action):

    def name(self) -> Text:
        return "action_busy_reply"

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

        replies = {'pa_plan_coverage': 'utter_chloe_pa_coverage',
                   'objection_already_have_PA_plan': 'chloe_had_a_pa_plan',
                   'nlu_fallback': 'utter_fallback',
                   'fees_question': 'chloe_pa_fees',
                   'question_related_to_scam': 'utter_chloe_scam',
                   'call_back_to_another_party': 'chloe_call _back_other',
                   'question_related_to_numbers': 'chloe_number_info',
                   'looking_for': 'chloe_looking_for'
                   }

        print('action_busy_reply', only_intents, only_actions)
        for intent, ans in replies.items():
            if intent == only_intents[-1]:
                reply = ans
                break
            else:
                reply = 'utter_chloe_goodbye'

        if only_intents.count('busy') > 1:
            reply = 'utter_chloe_goodbye'
        dispatcher.utter_message(response=reply)
        return []
