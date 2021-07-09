from typing import Container
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as dhtml
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("singapore-residents-by-ethnic-group-and-sex-end-june-annual.csv")
df['value']=pd.to_numeric(df['value'], errors='coerce')
df = df.groupby(['year','level_1'])[['value']].sum()
df.reset_index(inplace=True)
print(df[:5])
ethnic_list = ["Total Malays", "Total Chinese", "Total Indians", "Other Ethnic Groups (Total)"]


#-----app layout---------
app.layout = dhtml.Div([

    dhtml.H1("Web Application using Dash", style={"text-aling":"center"}),
    dcc.Dropdown(id="slct_factor",
                options=[
                    {"label":x, "value":x} for x in ethnic_list],
                multi=False,
                value="Total Malays",
                style={"width":"40%"}
    ),
    dhtml.Div(id="output_container",children=[]),
    dhtml.Br(),
    dcc.Graph(id="gender_line", figure={})
])

#-------------------------------
# connect plotly bars with dash components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='gender_line', component_property='figure')],
    [Input(component_id='slct_factor', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container= "The ethnic group selected was {}".format(option_slctd)
    dff = df.copy()
    dff = dff[dff['level_1']==option_slctd]

    fig = px.line(
        data_frame=dff,
        x='year',
        y='value',
        hover_data=['year','value'],
        color='level_1',
        template="plotly_dark"
    )

    return container, fig
    #return fig

#----------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)