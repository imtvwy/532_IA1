import pandas as pd
import altair as alt
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data

alt.data_transformers.enable('data_server')


# read data
df = pd.read_csv("../data/case_data.csv")

startDate="2021-01-01"
endDate="2021-01-31" 


# filter by date
mask = ((df["Reported_Date"] > startDate) &(df["Reported_Date"] <= endDate))
df_filtered = df.loc[mask]


# plot the time chart
def plot_altair(fill):
    chart = (alt.Chart(df_filtered, 
        title="Number of COVID19 cases over time")
                .mark_line().encode(
                    x=alt.X("Reported_Date",
                            title="Date"),
                    y=alt.Y("count()",
                            title="Number of Cases"),
                    color=alt.Color(fill,
                                    title=fill))
                )
    return chart.to_html()
        

app = Dash(__name__)

app.layout = html.Div([
        dcc.Dropdown(
            id='fill', value='HA',
            options=[{'label': 'HA', 'value': 'HA'}, {'label': 'Sex', 'value': 'Sex'}, {'label': 'Age_Group', 'value': 'Age_Group'}],
            style={'border-width': '0', 'width': '30%', 'height': '10px'}),

        html.Iframe(
            id='line',
            style={'border-width': '0', 'width': '100%', 'height': '400px'},
            srcDoc=plot_altair('HA'))])

@app.callback(
    Output('line', 'srcDoc'),
    Input('fill', 'value'))
def update_output(fill):
    return plot_altair(fill)


print(df)

if __name__ == '__main__':
    app.run_server(debug=True)