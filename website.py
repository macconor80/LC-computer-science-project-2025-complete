from flask import Flask, render_template
import sqlite3
import pandas as pd
import csv
import numpy as np
import plotly.express as px


website = Flask(__name__)

@website.route('/')
def home():
    # respose should be certain datatype - text is good
    return render_template('index.html')

@website.route('/foo')
def foo():
    page_name = 'Foo'
    return render_template('foo.html', page_name=page_name)


@website.route('/Graphs')
def graphs():
    with open('premier_league_teams_fixtures_clean_data.csv', mode='r') as infile:
        data = pd.read_csv(infile, encoding='utf-8')

    non_numeric_cols = ['HomeTeam', 'AwayTeam', 'FTR', 'HTR']

    stats_dictionary = {}

    for col in data.columns: #going through each column
        if col not in non_numeric_cols: #skipping columns we dont want to calculate
            stats_data = data[col] #lets call it stats data

            #populates stats dictionary
            stats_dictionary[col] = {
                "Mean" : stats_data.mean(),#get mean of column
                "Median" : stats_data.median(),# get median of column
                "Mode" : stats_data.mode().iloc[0] if not stats_data.mode().empty else np.man,#get mode if wanted
                "Range" : stats_data.max() - stats_data.min()#get range of column
            
        }

    #print(stats_dictionary)

    #convert stats to dataframe 
    stats_df = pd.DataFrame(stats_dictionary).transpose()
    # print(stats_df)


    ############## Basic requirement 2 create graphs using plotly

    #graph 1 bar chart: HomeTeam vs HomeTeam shots 
    bar_chart  =  px.bar(
        data,
        x=data.columns[1],
        y=data.columns[9],
        title="Bar Chart: Home Team vs Home Team shots",
        labels={data.columns[1]: "HomeTeam", data.columns[9]: "HomeTeam Shots per game"}
    )
    bar_chart.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    bar_chart_html = bar_chart.to_html(full_html=False, include_plotlyjs="cdn")

    #Graph 2 Scatter chart
    scatter_chart  =  px.scatter(
        data,
        x=data.columns[2],
        y=data.columns[18],
        title="Line plot AwayTeam vs AwayTeam Yellow cards",
        labels={data.columns[2]: "AwayTeam", data.columns[18]:"AwayTeam Yellow cards"}
    )
    scatter_chart.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    scatter_plot_html = scatter_chart.to_html(full_html=False, include_plotlyjs="cdn")
    
    #Graph 3 pie chart
    # get a copy of the dataframe
    pie_data = data.copy()
    pie_data = pie_data.filter(['HomeTeam', 'FTHG'])
   
    pie_chart = px.pie(pie_data, names="HomeTeam", values="FTHG", title="Pie Chart HomeTeam vs FullTime Home goals")
    pie_chart_html = pie_chart.to_html(full_html=False)

#show graphs in safari, chrome or excel
    return render_template(
        'graphs.html',
        bar_chart=bar_chart_html,
        pie_chart=pie_chart_html,
        scatter_chart=scatter_plot_html

    )

if __name__ == '__main__':
    website.run(debug=True, host='0.0.0.0')
