import dash
from dash import html
import plotly.graph_objects as go
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv('sentiment_cleaned.csv', lineterminator='\n')

app = dash.Dash()

app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Twitter Sentiment Analysis', style = {'textAlign':'center',\
                                            'marginTop':40,'marginBottom':40}),

        dcc.Dropdown(id = 'dropdown',
                     options = list(df['Hashtag'].unique()),
                     value = '#Apple'),
        dcc.Graph(id = 'sentiment_plot'), 
        dcc.Graph(id = 'counts_plot')
    ])
    
    
@app.callback(Output(component_id='sentiment_plot', component_property= 'figure'),
              Output(component_id='counts_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def graph_update(hashtag):
    print(hashtag)
    
    df_hashtag = df[df['Hashtag']==hashtag][['Date', 'Label']]
    df_hashtag = df_hashtag.sort_values('Date', ascending=True).reset_index(drop=True)
    df_hashtag['MA Sentiment'] = df_hashtag['Label'].rolling(500, min_periods=100).mean()
    
    fig = go.Figure([go.Scatter(x = df_hashtag['Date'], y = df_hashtag['MA Sentiment'],\
                     line = dict(color = 'firebrick', width = 2))
                     ])
    
    fig.update_layout(title = 'Rolling Median Sentiment',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Sentiment'
                      )
    
    df_hist = df_hashtag['Label'].value_counts().reset_index().rename(columns={'index':'Label', 'Label':'Counts'})
    fig2 = go.Figure([go.Bar(x=df_hist['Label'], y=df_hist['Counts'])])
    
    fig2.update_layout(title = 'Sentiment Value Counts',
                       xaxis_title = 'Sentiment',
                       yaxis_title = 'Counts'
                       )
    fig2.update_xaxes(tickvals = ['Negative', 'Neutral', 'Positive'])
    
    return fig, fig2

if __name__ == '__main__': 
    app.run_server()