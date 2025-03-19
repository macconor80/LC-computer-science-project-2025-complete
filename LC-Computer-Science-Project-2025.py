#from gettext import npgettext
import pandas as pd
import numpy as np
from flask import Flask, app, render_template # type: ignore
import plotly.express as px
#basic requriement 1

#set the file path
file_path = 'premier_league_teams_fixtures_dirty_data.csv'

# Read the CSV file into a Pandas DataFrame, treating 'no data' as missing values  
data = pd.read_csv(file_path, encoding='utf-8')

# Remove special characters like # from all data values
data = data.replace({'#': ''}, regex=True)

# Drop rows that contain missing data to ensure clean analysis
data = data.dropna()

# Define columns to delete (update with actual column names to remove)
columns_to_delete = ['Date', 'Referee']  # Placeholder column names
# Remove specified columns if they exist, ignoring errors if they don't
data = data.drop(columns=columns_to_delete, errors='ignore')

#save cleaned data to new file
cleaned_file_path = 'premier_league_teams_fixtures_clean_data.csv'
data.to_csv(cleaned_file_path)

# FINISHED WRITING CSV

################basic requirement 2

#define non numeric columns so we can ignore
non_numeric_cols = ['HomeTeam', 'AwayTeam', 'FTR', 'HTR']

stats_dictionary = {}

for col in data.columns: #going through each column
    if col not in non_numeric_cols: #skipping columns we dont want to calculate"
        stats_data = data[col] #lets call it stats data

        #populates stats dictionary
        stats_dictionary[col] = {
            "Mean" : stats_data.mean(),#get mean of columns
            "Median" : stats_data.median(),#get the median of columns
            "Mode" : stats_data.mode().iloc[0] if not stats_data.mode().empty else np.man,#get mode if wanted
            "Range" : stats_data.max() - stats_data.min()#get range of columns
        
    }

#print(stats_dictionary)

#convert stats to dataframe 
stats_df = pd.DataFrame(stats_dictionary).transpose()
print(stats_df)


############## Basic requirement 2 create graphs  using plotly

#graph 1 bar chart: Hometeam 0 vs HomeTeam Shots per game
bar_chart  =  px.bar(
    data,
    x=data.columns[0],
    y=data.columns[8],
    title="Bar Chart: Home Team vs Home Team shots",
    labels={data.columns[0]: "HomeTeam", data.columns[8]: "HomeTeam Shots per game"}

)
bar_chart_html = bar_chart.to_html(full_html=False, include_plotlyjs="cdn")

#graph 2 AwayTeam vs Full Time away goals 16
scatter_chart  =  px.scatter(
    data,
    x=data.columns[1],
    y=data.columns[3],
    title="Scatter chart test: AwayTeam vs Full Time away goals",
    labels={data.columns[3]: "Away goals scored"}
)
scatter_chart_html = scatter_chart.to_html(full_html=False, include_plotlyjs="cdn")

#Graph 3 Line plot
line_plot = px.line(
    data,
    x=data.columns[0],
    y=data.columns[16],
    title="test line plot HomeTeam vs home Yellow cards",
    labels={data.columns[3]: "Home Yellow cards"}
)
line_plot_html = line_plot.to_html(full_html=False, include_plotlyjs="cdn")


#show graphs in safari, chrome or excel
bar_chart.show()
scatter_chart.show()
line_plot.show()


################################basic requirement 3 graphs on a webpage

# app = Flask(__name__)

# #routes
# @app.route('/')
# def index():
#     return render_template(
#         'index.html',
#         bar_chart=bar_chart_html,
#         scatter_chart=scatter_chart_html
#     )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
    