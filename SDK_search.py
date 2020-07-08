from azure.cognitiveservices.search.websearch import WebSearchClient
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials

""" subscription_key = "3d12a190762442a79e1099a8f8ab1a3f"
client = WebSearchClient(endpoint="https://chatbot-prototype-dev.cognitiveservices.azure.com", credentials=CognitiveServicesCredentials(subscription_key))

web_data = client.web.search(query=" ")

res_pages = web_data.web_pages.value """


def search_res(q, subscription_key="3d12a190762442a79e1099a8f8ab1a3f", endpoint="https://chatbot-prototype-dev.cognitiveservices.azure.com"):
    client = WebSearchClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key))

    web_data = client.web.search(query=q)
    res_pages = web_data.web_pages.value

    return res_pages