from rasa_core.actions import Action
import kanbanConstants as K
import utils

current_index = 0

# get the next key to explain
def getNextKanbanKey(index):
    try:
        key = K.kanbanGeneralKeys[index]
        return key
    except IndexError:
        return None

# find a specific key to explain
def findKanbanKey(key):
    if key in K.kanbanGeneralKeysValues:
        return key
    else if key in K.kanbanDetailsKeysValues:
        return key
    else:
        return None

# ask to continue to the next key
class Continue(Action):
    def name(self):
        return 'continue'

    def run(self, dispatcher, tracker, domain):
        global current_index
        # increment current index
        current_index += 1
        # find the next key
        next_key = getNextKanbanKey(current_index)
        # make it the current one
        current_key = net_key
        # if all themes are explained end the guide otherwise ask for the next one
        if not current_key:
            response = 'That is it for the crash course in kanban. Would you like to restart?'
            current_key = K.kanbanGeneralKeys[0]
        else:
            response = 'Would you like to know about ' + current_key + '?'

        dispatcher.utter_message(utils.prepare_action_response(self.name(), tracker, response))
        return []


class Explain(Action):
    def name(self):
        return 'explain'

    def run(self, dispatcher, tracker, domain):
        global current_index

        if tracker.latest_message.parse_data['intent']['name'] == 'switch_kanban':
            current_key = K.kanbanGeneralKeys[0]
        else:
            current_key = K.kanbanGeneralKeys[current_index]

        # explain the current key
        dispatcher.utter_message(utils.prepare_action_response(self.name(), tracker, K.kanbanGeneralKeysValues[current_key]))
        return []


class ExplainDetail(Action):
    def name(self):
        return 'explain_detail'

    def run(self, dispatcher, tracker, domain):
        global current_index

        if tracker.latest_message.parse_data['intent']['name'] == 'switch_kanban':
            current_detail_keys = kanbanDetailsKeys[0]
        else:
            current_detail_keys = kanbanDetailsKeys[current_index]

        # explain the current key details
        for detail in current_detail_keys:
            dispatcher.utter_message(utils.prepare_action_response(self.name(), tracker, K.kanbanDetailsKeysValues[detail]))
        return []

class ExplainSpecific(Action):
    def name(self):
        return 'explain_specific'

    def run(self, dispatcher, tracker, domain):
        # get the theme entity from the console
        key = tracker.get_slot('theme')
        # check if it exists in kanban
        kanban_key = findKanbanKey(key)
        # build response
        if not kanban_key:
            response = "That term does not belong to the kanban framework"
        else:
            response = 'Here is what I found' + '\n' + kanban_key
        dispatcher.utter_message(utils.prepare_action_response(self.name(), tracker, response))
        return []
