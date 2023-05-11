#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Last updated: on Wednesday Apr 18 17:03 2022

@author: Ethan Masters

Purpose: Article Data Visualization Script

Python Version: Python 3.9.13 (main, Aug 25 2022, 18:29:29) 
"""

### Final Script NP Research ###


############## - Nuclear Proliferation Research - #############

### - IMPORTS - ###

from datetime import datetime
from datetime import timedelta
import os
import json
from pprint import pprint
import requests, re
import pandas as pd
import numpy as np
import time
import plotly.express as px

### - IMPORTS (END) - ###

### - Interested in Years 1945 - 2022 - ###

APIkey = "9jleO955LNYEMxbaH5A49adGcBJle43K" # Ethan's Key

test = 6

def ResearchNYT(startYear,endYear, collection=False):

    if collection == True:
        apiData = {}
        for year in range(startYear,endYear): 
            apiData[year] = {}
            for month in range(1,13): 
                apiData[year][month] = [requests.get(f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={APIkey}').json()]
                time.sleep(2)
            pprint(year)

        df = pd.DataFrame.from_dict(apiData, orient='index')
        df.to_json(fr"C:\Users\ethan\OneDrive\Desktop\ResearchRawData\NYT_API_DataFrame({startYear}-{endYear}).json")

    cwd = os.getcwd()
    df = pd.read_json(cwd + fr'/ResearchRawData/NYT_API_DataFrame({startYear}-{endYear}).json')
    
    ######## - DATA CLEANING - ########

    ### - FIRST PAGE ARTICLES - ###

    def tryArticle(article):

        pub_date = article['pub_date']
        pub_date = re.search(r'(\d{4})-\d{2}-\d{2}T',pub_date).group(1)

        if int(pub_date) <= 1980:
            try:
                if article["print_page"] == "1":
                    return article
            except:
                pass
        else:
            try:
                if (article['news_desk'] == 'Foreign Desk' or article['news_desk'] == 'Foreign') or (article['news_desk'] == 'National Desk' or article['news_desk'] == 'National'):
                    if article["print_page"] == "1":
                        return article
            except:
                pass

    def first_page(adict):
        return [article for article in adict[0]["response"]["docs"] if tryArticle(article)]

    ### - FIRST PAGE ARTICLES (END) - ###

    ### - ALL ARTICLES - ###

    def cleanData(adict):
        return [article for article in adict["response"]["docs"]]

    ### - ALL ARTICLES (END) - ###

    ######## - DATA CLEANING (END) - ########

    ######## - Data Cleaning regex search pattern to find target topics - ########

    ### - TOPIC CAPTURE CODE - ###
    def tryTopicFilter(article):
        pub_date = article['pub_date']
        pub_date = re.search(r'(\d{4})-\d{2}-\d{2}T',pub_date).group(1)

        total_capture = ["arms control and limitation and disarmament","strategic arms reduction treaty","nuclear nonproliferation treaty","eisenhower plan ('atoms for peace')","arms control","weapons disarmament"]

        if int(pub_date) <= 1966:
            capture_words = ["weapons disarmament","arms reduction","arms control","arms unification","disarmament","arms inspection"] # ENTER KEYWORDS HERE (maybe 'arms unification')
        else:
            capture_words = ["weapons disarmament","arms reduction","arms control","arms unification"] # ENTER KEYWORDS HERE (maybe 'arms unification')

        if article["keywords"]:
            article_subject = re.sub(r"\s+"," "," ".join([subject["value"] for subject in article["keywords"] if subject['name'] == "subject"]).lower())
            for first_capture in total_capture:
                if first_capture in article_subject:
                    return article

        for word in capture_words:
            if article['abstract']:
                abstract = re.sub(r"\s+"," ",article['abstract'].lower())
                if re.search(fr"{word}",abstract):
                    return article
            if article["snippet"]:
                snippet = re.sub(r"\s+"," ",article["snippet"].lower())
                if re.search(fr"{word}",snippet):
                    return article
            if article["headline"]:
                if article["headline"]["main"]:
                    main = re.sub(r"\s+"," ",article["headline"]["main"].lower())
                    if re.search(fr"{word}",main):
                        return article
                if article["headline"]["print_headline"]:
                    print_headline = re.sub(r"\s+"," ",article["headline"]["print_headline"].lower())
                    if re.search(fr"{word}",print_headline):
                        return article
            if article["lead_paragraph"]:
                lead_paragraph = re.sub(r"\s+"," ",article["lead_paragraph"].lower())
                if re.search(fr"{word}",lead_paragraph):
                    return article
            if article["keywords"]:
                article_subject = re.sub(r"\s+"," "," ".join([subject["value"] for subject in article["keywords"] if subject['name'] == "subject"]).lower())
                if re.search(fr"{word}",article_subject):
                    return article

    def topicFilter(adict):
        if adict == "None":
            return np.nan
        return [article for article in adict if tryTopicFilter(article)]
    ### - TOPIC CAPTURE CODE (END) - ###

    ### - Function Calls - ###
    df = df.applymap(first_page)
    df = df.applymap(topicFilter)
    ### - Function Calls (END) - ###

    ######## - Data Cleaning regex search pattern to find target topics (END) - ########

    return df

########################### - FUNCTION CALLS FULL DATAFRAME - ################################

def execute(cwd, test1 = test):

    def function_call(test_bool=False):
        df = pd.DataFrame()

        for year in range(1945,2022):
            if test_bool == True:
                ResearchNYT(year,year+1)
                break
            if df.empty:
                df = ResearchNYT(year,year+1)
                pprint('First Iteration')
            else:
                df = pd.concat([df,ResearchNYT(year,year+1)])
                pprint(year)
        
        return df

    output_data = function_call()

    def cleaning_data(input_data):
        input_data = input_data.values.tolist()
        data_dict = {}
        for year in input_data: # for row in df
            if not year:
                continue
            for month in year: # for value in row
                if not month:
                    continue
                for article in month: # for article in 
                    if not article:
                        continue
                    date = article["pub_date"]
                    if re.search(r"(\d{4})-",article["pub_date"]).group(1) in data_dict:
                        if article["pub_date"] in data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)]:
                            data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)][date + article["headline"]["main"][:8]] = article # added the last indexing to shorten publication date id for when duplicate
                        else:
                            data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)][date] = article

                    else:
                        data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)] = {}
                        data_dict[re.search(r"(\d{4})-",article["pub_date"]).group(1)][date] = article

        return data_dict

    output = cleaning_data(output_data)

    output_data = pd.DataFrame.from_dict({(i,j): output[i][j]
                            for i in output.keys() 
                            for j in output[i].keys()},
                        orient='index')

    final_output = output_data.rename_axis(['Year','Publication Date']).sort_index()

    def date_cleaning(value):
        month_dictionary = {'01':'January','02':'Feburary','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
        return month_dictionary[value]

    pub_date = final_output["pub_date"].str.split("-", expand = True)
    pub_date.drop([2],axis=1,inplace=True)
    pub_date.columns = ["Year","Month"]
    pub_date['Month Published'] = pub_date["Month"].apply(date_cleaning)
    final_output["Year Column"], final_output["Month"], final_output["Month Numeric"] = pub_date.values.T

    def subject_cleaning(alist):
        if alist:
            return str([adict['value'] for adict in alist if adict['name'] == 'subject'])
    
    def headline_main_cleaning(adict):
        if adict:
            return adict['main']

    def headline_print_line_cleaning(adict):
        if adict:
            return adict['print_headline']

    def link_formating(link):
        return f"[Article Link]({link})"

    final_output['subject'] = final_output['keywords'].apply(subject_cleaning)
    final_output['main_line'] = final_output['headline'].apply(headline_main_cleaning)
    final_output['print_headline'] = final_output['headline'].apply(headline_print_line_cleaning)
    final_output['web_url'] = final_output['web_url'].apply(link_formating)

    final_output.to_json(cwd + fr"/np_research_app/assets/df_regex_data_final_output_{test1}_.json", orient = 'table')

    return final_output

def data_test(cwd,test1 = test):

    final_nyt_output = pd.read_json(cwd + fr"/assets/df_regex_data_final_output_{test1}_.json", orient='table')
    article_occurences_df = pd.DataFrame(final_nyt_output.groupby(level=['Year']).size())
    article_occurences_df.reset_index(inplace=True)
    article_occurences_df.columns = ["Year","Article Count"]
    year_df = pd.read_json(cwd + "/assets/article_count_Per_Year1_.json")
    year_df.drop([2022,2023], axis=0, inplace=True)
    year_df.columns = ['Article_Count']
    article_occurences_df['year_occurence'] = year_df['Article_Count'].astype("int").values
    article_occurences_df['normalized'] = article_occurences_df.apply(lambda row: row['Article Count'] / row.year_occurence * 100 , axis=1)
    article_occurences_df.to_json(cwd + f"/assets/normalized_data_regex_test_{test1}_.json")
    template = "plotly_dark"
    px.bar(article_occurences_df,x="Year", y="normalized",title=f"Time Series Data Articles/Year Test: {test}",labels={"variable":"Key"},template=template).show()

def data_visualization(cwd):
    
    final_output = pd.read_json(cwd + f"/assets/df_regex_data_final_output_{test}_.json", orient='table')

    article_occurences_df = pd.DataFrame(final_output.groupby(level=['Year']).size())
    article_occurences_df.reset_index(inplace=True)
    article_occurences_df.columns = ["Year","Article Count"]

    template = "plotly_dark"
    px.line(article_occurences_df,x = "Year",y = "Article Count", title=f"Time Series Data Articles/Year Test: {test}",template=template).show()
    px.bar(article_occurences_df,x="Year", y="Article Count",title=f"Time Series Data Articles/Year Test: {test}",labels={"variable":"Key"},template=template).show()
    px.scatter(article_occurences_df,x="Year", y="Article Count", marginal_y="box",title=f"Time Series Data Articles/Year Test: {test}",labels={"variable":"Month"},template=template).show()

if __name__ == '__main__':
    cwd = os.getcwd()
    # final_output = execute()
    data_visualization(cwd)
    data_test(cwd)
    pass

def nyt_regex_module(test1=test):
    return pd.read_json(fr"assets/df_regex_data_final_output_{test}_.json", orient='table')