import os
from slack import WebClient
from slack.errors import SlackApiError
from slackeventsapi import SlackEventAdapter

#from search import search
from SDK_search import search_res
import json
import re

def construct_blocks(res_pages):
    res_blocks = []
    for i in range(len(res_pages)):
        block = {}
        block['type'] = 'section'
        block['text'] = {}
        block['text']['type'] = 'mrkdwn'
        block['text']['text'] ='*' + str(i) + ' ' + res_pages[i].name + '*' + '\n' + res_pages[i].snippet + '\n' + res_pages[i].display_url
        divider = {}
        divider['type'] = 'divider'
        res_blocks.append(block)
        res_blocks.append(divider)
    return res_blocks

# expand query based on relevance feedback
def query_expand(query, rf):
    query_base = log['query']
    res_page = log['res']
    for i in rf:
        query_base+=res_page[int(i)].snippet[:20]
    return query_base





# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events")

users = [] # contain the user id
log = {} # perserve last search log for relevance feedback.
pattern = re.compile(r'\d+')

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    user_id = message.get('user')
    rf = []
    # if message is not posted by user, do not react.
    if len(users) == 0:
        users.append(user_id)

    if message.get("subtype") is None and user_id in users:
        query = message.get("text")

        # if user input is about relevance feedback, then use rf to expand query.
        rf = pattern.findall(query)
        if len(rf):
            query = query_expand(rf, query)



        print(query)
        
        res_pages = search_res(query)
        log['query'] = query
        log['res'] = res_pages

        display_res_pages = res_pages
        #print(display_res_pages)
        display_res_pages_blocks = construct_blocks(display_res_pages)
        #print(display_res_pages_blocks)
        try:
            response = slack_web_client.chat_postMessage(
                channel = message['channel'],
                text = "search result of {}: ".format(query),
                blocks = display_res_pages_blocks
            )
        except SlackApiError as e:
            print(f"API Error: {e.response['error']}")
    
# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("Error Event: " + str(err))

# Start the server on port 3000
slack_events_adapter.start(port=3000)