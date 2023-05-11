## capturing articles per year

import requests
from pprint import pprint
import pandas as pd
import time
import pickle
import os


APIkey = "9jleO955LNYEMxbaH5A49adGcBJle43K" # Ethan's API Key

def collection(APIkey = APIkey):

    cwd = os.getcwd()

    article_Count = {}

    for year in range(1945,2024):

        start = f'{year}0101'
        end = f'{year}1231'
        requestUrl = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={start}&end_date={end}&sort=newest&api-key={APIkey}"

        response = requests.get(requestUrl).json()["response"]
        article_Count[year] = response['meta']['hits']

        time.sleep(2)

        pprint(year)

    with open(cwd + "/assets/yeardata.pkl", "wb") as f:
        pickle.dump(article_Count, f)

def execute():

    cwd = os.getcwd()

    with open(cwd + "/assets/yeardata.pkl", "rb") as f:
        article_Count = pickle.load(f)

    
    df = pd.DataFrame.from_dict(article_Count,orient='index')

    df.to_json(cwd + "/assets/article_count_Per_Year1_.json")

    pprint(df)


if __name__ == "__main__":
#   collection()
  execute()


