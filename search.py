import requests
import json


def resProcess(res):
    res_blocks = []
    """ res_blocks['text'] = "search result:"
    res_blocks['blocks']=[] """
    for i in range(len(res)):
        block = {}
        block['type'] = 'section'
        block['text']={}
        block['text']['type']='mrkdwn'
        block['text']['text']='*'+res[i]['name'].replace('<b>', '*').replace('</b>', '*').replace('&#39','\'')+'*'+'\n'+res[i]['url']+'\n'+res[i]['snippet'].replace('<b>', '*').replace('</b>', '*').replace('&#39','\'')
        res_blocks.append(block)
        j_res_blocks = json.dumps(res_blocks, ensure_ascii=False)
    return j_res_blocks

        
def search(search_term,subscription_key="3d12a190762442a79e1099a8f8ab1a3f",search_url="https://api.cognitive.microsoft.com/bing/v7.0/search"):
    headers = {
        "Ocp-Apim-Subscription-key": subscription_key
    }
    params = {
        "q": search_term,
        "textDecorations": True,
        "textFormat": "HTML"
    }

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
  """   serp = search_results['webPages']['value'][:10]
    res = resProcess(serp) """

    return search_results