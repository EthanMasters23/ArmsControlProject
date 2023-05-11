
### - IMPORTS - ###

import json
from pprint import pprint
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go

import os

### GUI imports ###
import dash
from dash import html
from dash import dcc
from dash import dash_table, callback
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

from plotly.subplots import make_subplots

########### - GUI - #############

cwd = os.getcwd()

if __name__ == "__main__":

    ### nyt api search ###
    # test = 15
    # final_output = article_api_module()
    # full_data_df = final_output.copy()
    # final_output = final_output.drop(["keywords","headline","Year Column","Month","Month Numeric","snippet","print_page","document_type","print_section","section_name","source"], axis=1)

    ### nyt regex search ###
    test = 6
    final_output = pd.read_json(cwd + f"/assets/df_regex_data_final_output_{test}_.json", orient='table')
    full_data_df = final_output.copy()
    final_output = final_output.drop(["keywords","headline","Year Column","Month","Month Numeric",'byline','multimedia','snippet','lead_paragraph','source','print_page','document_type','_id','word_count','uri','news_desk','section_name','type_of_material','_id','print_section','subsection_name','main_line'], axis=1)
    # final_output = final_output.drop(["keywords","headline","Year Column","Month","Month Numeric",'byline','multimedia','snippet','lead_paragraph'], axis=1)
    
    normalized_data = pd.read_json(cwd + f"/assets/normalized_data_regex_test_{test}_.json")

    pass

else:

    ### nyt api search ###
    # final_output = article_api_module()
    # full_data_df = final_output.copy()
    # final_output = final_output.drop(["keywords","headline","Year Column","Month","Month Numeric","snippet","print_page","document_type","print_section","section_name","source"], axis=1)

    ### nyt regex search
    test = 6
    final_output = pd.read_json(cwd + f"/assets/df_regex_data_final_output_{test}_.json", orient='table')
    full_data_df = final_output.copy()
    final_output = final_output.drop(["keywords","headline","Year Column","Month","Month Numeric",'byline','multimedia','snippet','lead_paragraph','source','print_page','document_type','_id','word_count','uri','news_desk','section_name','type_of_material','_id','print_section','subsection_name','main_line'], axis=1)

    ### normalized data
    normalized_data = pd.read_json(cwd + f"/assets/normalized_data_regex_test_{test}_.json")

    pass

### polling occurence graph ###

cwd = os.getcwd()
datapath = cwd + "/assets"
file = 'clean_polling_data_cleaned' + '.csv'
# file = 'clean_roper-folder-toplines-asof-20230127' + '.csv'
polling_df_o = pd.read_csv(datapath + "/" + file)
polling_df_o = polling_df_o.drop(['Unnamed: 0','ReleaseDate','QuestionID','QuestionNote','SubPopulation','SurveySponsor','SourceDoc','BegDate','EndDate','ExactDates','SampleDesc','IntMethod','StudyNote'],axis=1)
polling_df_o.columns = ['Response Text','Response %','Question Text','Survey Org','Sample Size', 'Year']
polling_df_o = polling_df_o.sort_values('Year')

polling_df = polling_df_o.groupby(["Year"]).size().reset_index()
polling_df.columns = ['year','count']

### article occurence graph ###

article_occurences_df = pd.DataFrame(final_output.groupby(level=['Year']).size())
article_occurences_df.reset_index(inplace=True)
article_occurences_df.columns = ["Year","Article Count"]

template = "ggplot2"

fig_polling_data = px.bar(polling_df,x="year", y="count",title="Survey's per Year (1945 - 2022)",labels={"variable":"Key"},template=template)

fig_normalized_data = px.bar(normalized_data,x="Year", y="normalized",title=f"Articles per Year NORMALIZED (1945 - 2022) (Test: {test})",labels={"variable":"Key"},template=template)

fig = px.bar(article_occurences_df,x="Year", y="Article Count",title=f"Articles per Year (1945 - 2022) (Test: {test})",labels={"variable":"Key"},template=template)

app = dash.Dash(__name__)

server = app.server

app.title = "Arms Control Project"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Arms Control Public Opinion", className="header-title", style = {'color': '#000000','font-size': '48px','font-weight': 'bold','text-align': 'center','margin': '0 auto'}
                ),
                html.P(
                    children="Search for a Year and Month"
                    " to launch data for that specific period"
                    " (You can select just one parameter for the search)",
                    className="sub-header-description", style={'text-align':'center','color':'#000000'}
                )
            ],
            className="header",
            style = {'background-color': '#F7F7F7','height': '240px','padding': '16px 0 0 0'}
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Year", className="menu-title",style={"text-align":'center'}),
                        dcc.Dropdown(
                            id="year-filter",
                            options=[ 
                                {"label": state, "value": state}
                                for state in np.sort(full_data_df["Year Column"].unique())
                            ],
                            placeholder ="Year",
                            multi=True,
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                    style={"width": "100px"},
                ),
                html.Div(
                    children=[
                        html.Div(children="Month", className="menu-title",style={"text-align":'center'}),
                        dcc.Dropdown(
                            id="month-filter",
                            options=[
                                {"label": city, "value": city}
                                for city in np.sort(full_data_df["Month Numeric"].unique())
                            ],
                            placeholder = "Month",
                            multi=True,
                            clearable=True,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                    style={"width": "100px"}
                ),
            ],
        className="menu",
        style = {
            'height': 'auto',
            'width': '300px',
            'display': 'flex',
            'justify-content': 'space-around',
            'margin': '-125px auto 0 auto',
            'background-color': '#FFFFFF',
            'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',
            'padding': '25px'
        }
        ),
        html.Div(id='result',className="Results",style={'text-align':'center','font-size' : '48px','font-weight':'bold','color' : 'black','margin-bottom': '0px','margin-top': '30px'}),
        dcc.Graph(id='graph'),
        html.P(
                    children=f"NYT Articles Found Between 1945 & 2022",
                    style={'text-align':'center','font-size' : '36px','font-weight':'bold','color' : 'black','margin-bottom': '0px','margin-top': '0px'},
                ),
        dcc.Graph(id='graph_done',figure=fig),
        dcc.Graph(id='graph_normalized_data',figure=fig_normalized_data),
        html.P(
                    children=f"Survey's Found Between 1945 & 2022",
                    style={'text-align':'center','font-size' : '36px','font-weight':'bold','color' : 'black','margin-bottom': '0px','margin-top': '0px'},
                ),
        dcc.Graph(id='graph_polling_data',figure=fig_polling_data),
        html.P(
                    children='Article & Survey Data',
                    style={'text-align':'center','font-size' : '36px','font-weight':'bold','color' : 'black','margin-bottom': '0px','margin-top': '0px'},
                ),
        html.P("Y-axis:",style={'margin-left':'57px'}),
        dcc.RadioItems(
            id='radio',
            options=['Article', 'Article & Survey'],
            value='Article & Survey',
            style={'margin-left':'50px'}
        ),
        dcc.Graph(id="graph_stat"),
        html.P(
                    children=f"NYT Articles Meta Data",
                    style={'text-align':'center','font-size' : '36px','font-weight':'bold','color' : 'black','margin-bottom': '0px','margin-top': '0px'},
                ),
        html.Div(
            children=[
                html.Div([
                    dash_table.DataTable(
                    id='list',
                    columns=[{'name': i, 'id': i,'deletable': True, 'presentation': 'markdown'} for i in final_output.columns],
                    data = final_output.to_dict('records'),
                    tooltip_data=[
                        {
                            column: {'value': str(value), 'type': 'markdown'}
                            for column, value in row.items()
                        } for row in final_output.drop(["web_url"],axis=1).to_dict('records')
                    ],
                    tooltip_delay=0,
                    tooltip_duration=None,
                    tooltip_header={i: i for i in final_output.columns},
                    # row_deletable=True,
                    filter_action="native",
                    filter_options={"placeholder_text": "Filter column..."},
                    export_format = "csv",
                    export_headers='display',
                    # page_current=0,
                    page_size=500,
                    style_filter = {
                        'background': 'white', 
                        'color': 'black',
                    },
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white',
                        'fontWeight': 'bold',
                    },
                    style_data={
                        'backgroundColor': 'white',
                        'color': 'black',
                    },
                    style_cell={
                    #     # all three widths are needed
                        'minWidth': '0px', 'width': '20px', 'maxWidth': '70px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'text-align' : 'left',
                        'padding' : '10px',
                        'marginLeft': '40px', 'marginRight': '40px',
                    },
                    style_table={'overflowX': 'scroll'}, 
                ),
            ],style = {'marginLeft': '40px', 'marginRight': '40px','padding':'40px'}),

            # new line 
            html.P(
                    children=f"Polling & Survey Meta Data",
                    style={'text-align':'center','font-size' : '36px','font-weight':'bold','color' : 'black','margin-bottom': '0px','margin-top': '0px'},
                ),
            html.Div([
                    dash_table.DataTable(
                    id='list_random',
                    columns=[{'name': i, 'id': i,'deletable': True, 'presentation': 'markdown'} for i in polling_df_o.columns],
                    data = polling_df_o.to_dict('records'),
                    tooltip_data=[
                        {
                            column: {'value': str(value), 'type': 'markdown'}
                            for column, value in row.items()
                        } for row in polling_df_o.to_dict('records')
                    ],
                    tooltip_delay=0,
                    tooltip_duration=None,
                    tooltip_header={i: i for i in polling_df_o.columns},
                    # row_deletable=True,
                    filter_action="native",
                    filter_options={"placeholder_text": "Filter column..."},
                    export_format = "csv",
                    export_headers='display',
                    # page_current=0,
                    page_size=500,
                    style_filter = {
                        'background': 'white', 
                        'color': 'black',
                    },
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white',
                        'fontWeight': 'bold',
                    },
                    style_data={
                        'backgroundColor': 'white',
                        'color': 'black',
                    },
                    style_cell={
                    #     # all three widths are needed
                        'minWidth': '0px', 'width': '20px', 'maxWidth': '70px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'text-align' : 'left',
                        'padding' : '10px',
                        'marginLeft': '40px', 'marginRight': '40px',
                    },
                    style_table={'overflowX': 'scroll'}, 
                ),
            ],style = {'marginLeft': '40px', 'marginRight': '40px','padding':'40px'})
            
            ],
            className="wrapper",
        ),
        # html.Div(
        # html.Iframe(src="assets/NEXUS_Literature_Review.pdf",title = 'Nuclear Proliferation Report', style = {'width':'80%', 'text-align':'center', 'height':'1300px','margin':'0 auto'},allow='fullscreen'),
        # )
    ],
)

@app.callback(
    [Output('list', 'data'),
    Output('list', 'columns'),
    Output('result', 'children'),
    Output('graph', 'figure'),
    Output('list', 'tooltip_data'),
    Output('list', 'tooltip_delay'),
    Output('list', 'tooltip_header'),
    Output('list', 'tooltip_duration'),
    Output("graph_stat", "figure"),
    ],
    [
        Input("year-filter", "value"),
        Input("month-filter", "value"),
        Input("radio", "value"),
    ],
)

def multi_output(year, month, radio_value):

    final_output = pd.read_json(fr"assets/df_regex_data_final_output_{test}_.json", orient='table')
    final_output.drop(["keywords","headline","Year Column","Month","Month Numeric",'byline','multimedia','snippet','lead_paragraph','source','print_page','document_type','_id','word_count','uri','news_desk','section_name','type_of_material','_id','print_section','subsection_name','main_line'], axis=1,inplace=True)

    ### for the case no year or month is selected ###
    columns=[{'name': i, 'id': i,'deletable': True, 'presentation': 'markdown'} for i in final_output.columns]
    data = final_output.to_dict('records')
    tooltip_data=[
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in final_output.drop(["web_url"],axis=1).to_dict('records')
    ]
    tooltip_delay=0
    tooltip_duration=None
    tooltip_header={i: i for i in final_output.columns}
    figure = {}
    result = ''
    ### for the case no year or month is selected ###

    article_occurences_df = pd.DataFrame(final_output.groupby(level=['Year']).size())
    article_occurences_df.reset_index(inplace=True)
    article_occurences_df.columns = ["Year","Article Count"]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=normalized_data['Year'].tolist(), y=normalized_data['Article Count'].tolist(), # change Article Count to normalized for normalized comparison
        name="Article"), secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=polling_df['year'].tolist(), y=polling_df['count'].tolist(), name="Survey"),
        secondary_y=radio_value == 'Article & Survey',
    )

    # Add figure title
    fig.update_layout(title_text="Interactive Data-Scaling for Trend Observations")

    # Set x-axis title
    fig.update_xaxes(title_text="Year")

    # Set y-axes titles
    fig.update_yaxes(
        title_text="<b>Article</b> Article Occcurence Per Year", 
        secondary_y=False)
    fig.update_yaxes(
        title_text="<b>Survey</b> Survey Occurence Per Year", 
        secondary_y=True)

    if not year and not month:
        return data,columns,result,figure,tooltip_data,tooltip_delay,tooltip_header,tooltip_duration,fig
        # raise PreventUpdate

    # final_output = pd.read_json(f"assets/df_research_data_output_test_{test}_.json", orient='table')

    ### regex data ###
    final_output = pd.read_json(fr"assets/df_regex_data_final_output_{test}_.json", orient='table')
    final_output = final_output.drop(['keywords','headline','byline','multimedia','snippet','lead_paragraph','source','print_page','document_type','_id','word_count','uri','news_desk','section_name','type_of_material','_id','print_section','subsection_name','main_line'], axis=1)

    # template = "plotly_dark"
    template = "ggplot2"

    if year and month:
        final_output = final_output[final_output["Year Column"].isin(year)]
        final_output = final_output[final_output["Month Numeric"].isin(month)]
        final_output.drop(["Year Column","Month","Month Numeric"],axis=1,inplace=True)

        data = final_output.to_dict('records')
        columns = [{'name': i, 'id': i,'deletable': True, 'presentation': 'markdown'} for i in final_output.columns]
        count = final_output.shape[0]
        result = f"There were {count} Article(s) in {month} {year}"
        figure = {}

    elif year:
        final_output = final_output[final_output["Year Column"].isin(year)]
        article_occurences_df = pd.DataFrame(final_output.groupby(['Month Numeric']).size())
        article_occurences_df.reset_index(inplace=True)
        article_occurences_df.columns = ["Month","Article Count"]
        figure = px.bar(article_occurences_df,x="Month", y="Article Count",title=f"Articles From the year(s) {year} Grouped by Month (Test: {test})",labels={"variable":"Key"},template=template)

        final_output.drop(["Year Column","Month","Month Numeric"],axis=1,inplace=True)
        data = final_output.to_dict('records')
        columns = [{'name': i, 'id': i,'deletable': True, 'presentation': 'markdown'} for i in final_output.columns]
        count = final_output.shape[0]
        result = f"There were {count} Article(s) in {year}"

    elif month:
        final_output = final_output[final_output["Month Numeric"].isin(month)]
        article_occurences_df = pd.DataFrame(final_output.groupby(['Year Column']).size())
        article_occurences_df.reset_index(inplace=True)
        article_occurences_df.columns = ["Year","Article Count"]
        figure = px.bar(article_occurences_df,x="Year", y="Article Count",title=f"Articles From the month (s){month} Grouped by Years (Test: {test})",labels={"variable":"Key"},template=template)

        final_output.drop(["Year Column","Month","Month Numeric"],axis=1,inplace=True)
        data = final_output.to_dict('records')
        columns = [{'name': i, 'id': i,'deletable': True, 'presentation': 'markdown'} for i in final_output.columns]
        count = final_output.shape[0]
        result = f"There were {count} Article(s) in {month}"

    tooltip_data=[
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in final_output.drop(["web_url"],axis=1).to_dict('records')
    ]
    tooltip_delay=0
    tooltip_duration=None
    tooltip_header={i: i for i in final_output.columns}

    return data,columns,result,figure,tooltip_data,tooltip_delay,tooltip_header,tooltip_duration,fig,

if __name__ == "__main__":
    app.run_server(debug=True)