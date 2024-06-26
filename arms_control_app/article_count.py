import requests
import json
import pandas as pd
import time
import logging
from tqdm import tqdm
import os


class FetchTotalArticles:
    def __init__(self, API_KEY, START_YEAR, END_YEAR):
        self.API_KEY = API_KEY
        self.START_YEAR = START_YEAR
        self.END_YEAR = END_YEAR
        self.article_data = {}
        self.logger = logging.getLogger(type(self).__name__)
    
    def run(self):
        self.fetch_article_count()
        self.save_articles_total()
        self.load_articles_total()
        self.to_dataframe()
        self.to_json()

    def fetch_article_count(self):
        for year in tqdm(range(self.START_YEAR, self.END_YEAR + 1)):
            start = f'{year}0101'
            end = f'{year}1231'
            request_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={start}&end_date={end}&sort=newest&api-key={self.API_KEY}"
            self._processs_request(request_url, year)

    def _processs_request(self, url, year):
        for attempt in range(3):
            try:
                resp = requests.get(url)
                resp.raise_for_status()
                response = resp.json()["response"]
                self.article_data[year] = response['meta']['hits']
                time.sleep(2 * attempt + 2)
                return
            except (requests.RequestException, ValueError) as e:
                self.logger.error(f"Error fetching data retrying... : {e}")
            time.sleep(2 * attempt + 2)
        self.logger.error(f"Error failed to fetch data from {year} with url: {url}")

    def save_articles_total(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"NYT_Total_Article_Count_({self.START_YEAR}-{self.END_YEAR}).json")
        with open(file_path, "w") as f:
            json.dump(self.article_data, f)

    def load_articles_total(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"NYT_Total_Article_Count_({self.START_YEAR}-{self.END_YEAR}).json")
        try:
            with open(file_path, "r") as f:
                self.article_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    def to_dataframe(self):
        self.article_data = pd.DataFrame.from_dict(self.article_data, orient='index')

    def to_json(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"NYT_Total_Article_Count_DataFrame_({self.START_YEAR}-{self.END_YEAR}).json")
        self.article_data.to_json(file_path)

    def from_json(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'assets', f"NYT_Total_Article_Count_DataFrame_({self.START_YEAR}-{self.END_YEAR}).json")
        try:
            self.article_data = pd.read_json(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    def get_article_data(self):
        return self.article_data

if __name__ == "__main__":
    logging.basicConfig(filename='ArticleCountLog.log',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)
    start_time = time.time()

    pipeline = FetchTotalArticles(
        API_KEY = "9jleO955LNYEMxbaH5A49adGcBJle43K",
        START_YEAR = 1945,
        END_YEAR = 2024
    ).run()

    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Total runtime: {total_time:.2f}" + "\n"*4)



