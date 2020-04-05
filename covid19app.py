import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import dash_table


# external CSS stylesheets
external_stylesheets = [
   {
       'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
       'rel': 'stylesheet',
       'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
       'crossorigin': 'anonymous'
   }
]
# df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
dfc=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv').iloc[:,1:]
dfd=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv').iloc[:,1:]
dfr=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv').iloc[:,1:]


dfc.rename(columns={'Country/Region':'Country'},inplace=True)
dfd.rename(columns={'Country/Region':'Country'},inplace=True)
dfr.rename(columns={'Country/Region':'Country'},inplace=True)

trimc=dfc.groupby('Country').sum().reset_index()
trimd=dfd.groupby('Country').sum().reset_index()
trimr=dfr.groupby('Country').sum().reset_index()


#for the map

# dates = pd.DataFrame(df.columns[3:], columns=['Date'])
# countries=df.iloc[:,0:3]
# final=pd.DataFrame()
# df.rename(columns={'Country/Region':'Country'},inplace=True)
# for i in dates['Date']:
#     countries['Date']=i
#     a=df[['Country',i]]
#     confirmed=a.groupby('Country')[i].sum().reset_index().set_index('Country')
#     countries=countries.drop_duplicates(subset=['Country'])
#     x=countries.set_index('Country')
#     x['Confirmed']=confirmed
#     x=x.reset_index()
#     final=final.append(x,ignore_index=True)

# per_country=dfc.iloc[:,3:].sum(axis=0).reset_index()
# per_country[['Country','Lat','Long']]=dfc[['Country','Lat','Long']]
# per_date=dfc.iloc[:,3:].sum().reset_index().rename(columns={'index':'Date',0:'Confirmed'})

#animated map
# fig1 = px.scatter_geo(df, lat='Lat', lon='Long', locations="Country", locationmode='country names',color='Country',
#                      hover_name='Country',hover_data=['Confirmed'],size='Confirmed', size_max=25,
#                      animation_frame='Date',
#                      projection="natural earth")



# tracec= go.Scatter(x=dfc.sum()[3:].reset_index().iloc[:,0],
#                    y=dfc.sum()[3:].reset_index().iloc[:,1],
#                    mode='lines',
#                    marker={'color': '#a0065a'},
#                    name='Confirmed')
#
# traced= go.Scatter(x=dfd.sum()[3:].reset_index().iloc[:,0],
#                    y=dfd.sum()[3:].reset_index().iloc[:,1],
#                    mode='lines',
#                    marker={'color': '#6b6c6e'},
#                    name='Deceased')
#
# tracer= go.Scatter(x=dfr.sum()[3:].reset_index().iloc[:,0],
#                    y=dfr.sum()[3:].reset_index().iloc[:,1],
#                    mode='lines',
#                    marker={'color': '#1b63f2'},
#                    name='Recovered',)
#
# fig2=go.Figure(data=[tracec,traced,tracer], layout=go.Layout(title='Cumulative Number of Confirmed, Deceased and Recovered Cases',
#                    xaxis={'title': 'Date'},
#                    yaxis={'title': 'Number of People affected'}))

#Number of Confirms and Deaths
sums=dfc.sum()[3:]
diffsc=[]
for i in range(1,len(sums)):
    diffsc.append(sums[i]-sums[i-1])

sums=dfd.sum()[3:]
diffsd=[]
for i in range(1,len(sums)):
    diffsd.append(sums[i]-sums[i-1])

sums=dfr.sum()[3:]
diffsr=[]
for i in range(1,len(sums)):
    diffsr.append(sums[i]-sums[i-1])

#Worldwide trends of new confirms and deaths
fig3=go.Figure(data=[go.Bar(x=list(dfc.columns[4:]),
                            y=diffsc,
                            name='New Positive Cases'),
                     go.Bar(x=list(dfd.columns[4:]),
                            y=diffsd,
                            name='New Deaths'),
                            go.Bar(x=list(dfr.columns[4:]),
                            y=diffsr,
                            name='New Recovered Cases'),
                     ],
               layout=go.Layout(
                    title = 'Number of cases per day',
                   xaxis = {'title': 'Dates'},
                   yaxis = {'title': 'New cases per day'},
                   barmode='stack'))


options=[{'label':'All','value':'All'}]
for i in trimc['Country']:
    options.append({'label':i,'value':i})


#Card Values
total= trimc.iloc[:, -1].sum()+dfd.iloc[:,-1].sum()+dfr.iloc[:,-1].sum()
active=trimc.iloc[:, -1].sum()
deaths=dfd.iloc[:,-1].sum()
recovered=dfr.iloc[:,-1].sum()


#display table
display=pd.DataFrame(list(zip(trimc['Country'].values,trimc.iloc[:,-1].values,)),columns=['Country','Total Cases'])
x=[]
for i in range(0,len(trimc)):
    x.append(trimc.iloc[i,-1]-trimc.iloc[i,-2])
display['New Infections']=x

display['Total Deaths']=trimd.iloc[:,-1].values
x=[]
for i in range(0,len(trimd)):
    x.append(trimd.iloc[i,-1]-trimd.iloc[i,-2])
display['New Deaths']=x

display['Total Deaths']=trimr.iloc[:,-1].values
x=[]
for i in range(0,len(trimr)):
    x.append(trimr.iloc[i,-1]-trimr.iloc[i,-2])
display['New Recoveries']=x




app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server

app.layout = html.Div([
    html.Div(html.H1("Covid-19 Global Pandemic Live",style={'color':'#fff','text-align':'center','margin':15,'text-decoration':'underline'}),),
    html.Hr([],style={'border-top': '1px solid white', 'width':'50%'}),
    #cards
    html.Div([
        #cards
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className='text-light'),
                    html.H4(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className='text-light'),
                    html.H4(active, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Death Cases", className='text-light'),
                    html.H4(deaths, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovery Cases", className='text-light'),
                    html.H4(recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-3'),
    ], className='row', style={'margin':30}),
    html.Hr([], style={'border-top': '1px solid white', 'width': '80%',}),

    #graphs
    #map
    html.Div([
        # dcc.Graph(id='Map', figure=fig1)
    ]),
    #heatmap
    html.Div([
        # html.H4('Heatmap of current positive cases around the globe',style={'color':'#fff','text-align':'right','text-decoration':'underline'}),
        dcc.Graph(figure=px.density_mapbox(dfc, lat='Lat', lon='Long', z=dfc.columns[-1], radius=25,
                        # center=dict(lat=0, lon=180),
                              height=800,             zoom=1,
                        mapbox_style="stamen-terrain",
                        hover_name='Country',
                        labels={dfc.columns[-1]:'Current Cases'},
                        title='Heatmap of current positive cases around the globe'
                        ),
                  )
    ], style={'margin':40}),
    #Global Trends
    html.Div([

        html.Div([
            #dropdown
            html.Div([
        dcc.Dropdown(
            id='picker',
            options=[
                {'label': 'All (Logarithmic)', 'value': 'alllog'},
                {'label': 'All', 'value': 'all'},
                {'label': 'Confirmed', 'value': 'confirmed'},
                {'label': 'Deceased', 'value': 'deceased'},
                {'label': 'Recovered', 'value': 'recovered'},
            ],
            value='alllog'
        ),
        dcc.Graph(id='Cases')
    ],),
        ], className='col', style={'margin':5}),
        html.Div([
            #bar
            html.Div([
        dcc.Graph(figure=fig3)
    ],),
        ], className='col', style={'margin':5}),

    ], className='row', style={'padding':30}),
    html.Hr([], style={'border-top': '1px solid white', 'width': '80%', }),

    html.H2('Country-wise trends', style={'color':'#fff','text-align':'center','text-decoration':'underline','margin-top':15}),
    #dropdown country
    html.Div([
        dcc.Dropdown(id='country-picker', options=options, value='All'),
    ],style={'margin-bottom':0,'margin-top':15,'margin-left':35,'margin-right':35},),
    #graphs country
    html.Div([
        html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Logarithmic', 'value': 'log'},
                    {'label': 'Linear', 'value': 'lin'},
                ],
                value='lin',
                labelStyle={'display': 'inline-block'},
                id='radio',
                style={'color':'#fff'}
            ),
            dcc.Graph(id='country-case-cumulative'),
        ],className='col', style={'margin':5}),
        html.Div([
            dcc.Graph(id='country-case-daily'),
        ], className='col', style={'margin': 5}),
    ],className='row', style={'padding':30}),
    html.Hr([], style={'border-top': '1px solid white', 'width': '80%', }),

    #pie
    html.Div([
        html.H4('Total number of positive cases currently per country={}'.format(total),style={'color':'#fff','text-align':'right','text-decoration':'underline'}),
        dcc.Graph(figure=px.pie(trimc, values=trimc.iloc[:, -1], names='Country', hover_name='Country',),)
    ], style={'margin':40,'padding-left':40,'padding-right':40}),
    html.Hr([], style={'border-top': '1px solid white', 'width': '80%', }),

    #table
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in display.columns],
            data=display.to_dict('records'),
                # style_table={
                    # 'maxHeight': '50ex',
                    # 'overflowY': 'scroll',
                    # 'width': '100%',
                    # 'minWidth': '100%',
                # },
                # style cell
                style_cell={
                    'fontFamily': 'Open Sans',
                    'textAlign': 'center',
                    'height': '60px',
                    'padding': '2px 22px',
                    'whiteSpace': 'inherit',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'State'},
                        'textAlign': 'left'
                    },
                ],
                # style header
                style_header={
                    'fontWeight': 'bold',
                    'fontColor': 'white',
                    'backgroundColor': '#bec4d1',
                },
                # style filter
                # style data
                style_data_conditional=[
            {
                # stripped rows
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            # {
            #     # highlight one row
            #     'if': {'row_index': 0},
            #     "backgroundColor": "#3D9970",
            #     'color': 'white'
            # }
        ]
    )
    ],style={'padding':30,'margin':25}),


])

#For Country Specific trends
#Cumulative
@app.callback(Output('country-case-cumulative','figure'), [Input('country-picker','value'),Input('radio','value')])
def country_specific_cumulative(type, kind):
    # , Output('country-case-daily', 'figure')]
    if type in trimc['Country'].values and kind=='log':
        return {
           'data': [go.Scatter(x=list(trimc[trimc['Country']==type].iloc[:,3:].columns),
                               y=trimc[trimc['Country']==type].iloc[:,3:].values.tolist()[0],
                               mode='lines',
                               marker={'color': '#a0065a'},
                               name='Confirmed'),
                    go.Scatter(x=list(trimd[trimd['Country']==type].iloc[:,3:].columns),
                               y=trimd[trimd['Country']==type].iloc[:,3:].values.tolist()[0],
                               mode='lines',
                               marker={'color': '#6b6c6e'},
                               name='Deceased'),
                    go.Scatter(x=list(trimr[trimr['Country']==type].iloc[:,3:].columns),
                               y=trimr[trimr['Country']==type].iloc[:,3:].values.tolist()[0],
                               mode='lines',
                               marker={'color': '#1b63f2'},
                               name='Recovered', )
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Date'
               ),
               'yaxis': dict(
                   title='Number of people affected',
                    type='log',
               autorange=True

        ),
               'title': 'Cumulative Cases Confirmed, Deceased and Recovered'
           })
        }
    elif type in trimc['Country'].values and kind == 'lin':
        return {
            'data': [go.Scatter(x=list(trimc[trimc['Country'] == type].iloc[:, 3:].columns),
                                y=trimc[trimc['Country'] == type].iloc[:, 3:].values.tolist()[0],
                                mode='lines',
                                marker={'color': '#a0065a'},
                                name='Confirmed'),
                     go.Scatter(x=list(trimd[trimd['Country'] == type].iloc[:, 3:].columns),
                                y=trimd[trimd['Country'] == type].iloc[:, 3:].values.tolist()[0],
                                mode='lines',
                                marker={'color': '#6b6c6e'},
                                name='Deceased'),
                     go.Scatter(x=list(trimr[trimr['Country'] == type].iloc[:, 3:].columns),
                                y=trimr[trimr['Country'] == type].iloc[:, 3:].values.tolist()[0],
                                mode='lines',
                                marker={'color': '#1b63f2'},
                                name='Recovered', )
                     ],
            'layout': go.Layout({
                'xaxis': dict(
                    title='Date'
                ),
                'yaxis': dict(
                    title='Number of people affected',
                ),
                'title': 'Cumulative Cases Confirmed, Deceased and Recovered'
            })
    }
    elif type not in trimc['Country'].values and kind == 'log':
        return {
            'data': [go.Scatter(x=dfc.sum()[3:].reset_index().iloc[:, 0],
                                y=dfc.sum()[3:].reset_index().iloc[:, 1],
                                mode='lines',
                                marker={'color': '#a0065a'},
                                name='Confirmed'),
                     go.Scatter(x=dfd.sum()[3:].reset_index().iloc[:, 0],
                                y=dfd.sum()[3:].reset_index().iloc[:, 1],
                                mode='lines',
                                marker={'color': '#6b6c6e'},
                                name='Deceased'),
                     go.Scatter(x=dfr.sum()[3:].reset_index().iloc[:, 0],
                                y=dfr.sum()[3:].reset_index().iloc[:, 1],
                                mode='lines',
                                marker={'color': '#1b63f2'},
                                name='Recovered', )
                     ],
            'layout': go.Layout({
                'xaxis': dict(
                    title='Date'
                ),
                'yaxis': dict(
                    title='Number of people affected',
                    type='log',
                    autorange=True
                ),
                'title': 'Cumulative Cases Confirmed, Deceased and Recovered (Logarithm)'
            })
        }
    else:
       return {
           'data': [go.Scatter(x=dfc.sum()[3:].reset_index().iloc[:, 0],
                               y=dfc.sum()[3:].reset_index().iloc[:, 1],
                               mode='lines',
                               marker={'color': '#a0065a'},
                               name='Confirmed'),
                    go.Scatter(x=dfd.sum()[3:].reset_index().iloc[:, 0],
                               y=dfd.sum()[3:].reset_index().iloc[:, 1],
                               mode='lines',
                               marker={'color': '#6b6c6e'},
                               name='Deceased'),
                    go.Scatter(x=dfr.sum()[3:].reset_index().iloc[:, 0],
                               y=dfr.sum()[3:].reset_index().iloc[:, 1],
                               mode='lines',
                               marker={'color': '#1b63f2'},
                               name='Recovered', )
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Date'
               ),
               'yaxis': dict(
                   title='Number of people affected',
                   # type='log',
                   #  autorange='True'

       ),
               'title': 'Cumulative Cases Confirmed, Deceased and Recovered',
           })
       }

#daily
@app.callback(Output('country-case-daily', 'figure'), [Input('country-picker','value')])
def country_specific_daily(type):
   if type in trimc['Country'].values:
       sums = trimc[trimc['Country'] == 'India'].values.tolist()[0][3:]
       diffsc = []
       for i in range(1, len(sums)):
           diffsc.append(sums[i] - sums[i - 1])

       sums = trimd[trimd['Country'] == 'India'].values.tolist()[0][3:]
       diffsd = []
       for i in range(1, len(sums)):
           diffsd.append(sums[i] - sums[i - 1])

       sums = trimr[trimr['Country'] == 'India'].values.tolist()[0][3:]
       diffsr = []
       for i in range(1, len(sums)):
           diffsr.append(sums[i] - sums[i - 1])
       return {
           'data': [go.Bar(x=list(trimc.columns[4:]),
                            y=diffsc,
                            name='New Positive Cases'),
                     go.Bar(x=list(trimd.columns[4:]),
                            y=diffsd,
                            name='New Deaths'),
                    go.Bar(x=list(trimr.columns[4:]),
                            y=diffsr,
                            name='New Recovered Cases')
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Dates'
               ),
               'yaxis': dict(
                   title='New cases per day'
               ),
               'title': 'Number of cases per day',
               'barmode':'stack'
           })
       }
   else:
       sums = dfc.sum()[3:]
       diffsc = []
       for i in range(1, len(sums)):
           diffsc.append(sums[i] - sums[i - 1])

       sums = dfd.sum()[3:]
       diffsd = []
       for i in range(1, len(sums)):
           diffsd.append(sums[i] - sums[i - 1])

       sums = dfr.sum()[3:]
       diffsr = []
       for i in range(1, len(sums)):
           diffsr.append(sums[i] - sums[i - 1])
       return {

           'data': [go.Bar(x=list(dfc.columns[4:]),
                            y=diffsc,
                            name='New Positive Cases'),
                     go.Bar(x=list(dfd.columns[4:]),
                            y=diffsd,
                            name='New Deaths'),
                            go.Bar(x=list(dfr.columns[4:]),
                            y=diffsr,
                            name='New Recovered Cases'),
                    ],
           'layout': go.Layout({
               'xaxis': dict(
                   title='Dates'
               ),
               'yaxis': dict(
                   title='New cases per day'
               ),
               'title': 'Number of cases per day',
               'barmode':'stack'
           })
       }

#Global Trends
@app.callback(Output('Cases', 'figure'), [Input('picker', 'value')])
def totalcasegraphplot(type) :
    if(type == "alllog"):
        return {
            'data': [go.Scatter(x=dfc.sum()[3:].reset_index().iloc[:, 0],
                                   y=dfc.sum()[3:].reset_index().iloc[:,1],
                                   mode='lines',
                                   marker={'color': '#a0065a'},
                                   name='Confirmed'),
                     go.Scatter(x=dfd.sum()[3:].reset_index().iloc[:, 0],
                                y=dfd.sum()[3:].reset_index().iloc[:, 1],
                                mode='lines',
                                marker={'color': '#6b6c6e'},
                                name='Deceased'),
                     go.Scatter(x=dfr.sum()[3:].reset_index().iloc[:, 0],
                                y=dfr.sum()[3:].reset_index().iloc[:, 1],
                                mode='lines',
                                marker={'color': '#1b63f2'},
                                name='Recovered', )
                     ],
            'layout': go.Layout({
                'xaxis': dict(
                    title='Date'
                ),
                'yaxis':dict(
                    title='Number of people affected',
                    type='log',
                    autorange=True
                ),
                'title': 'Cumulative Cases Confirmed, Deceased and Recovered (Logarithm)'
            })
        }
    elif (type == "all"):
        return {
            'data': [go.Scatter(x=dfc.sum()[3:].reset_index().iloc[:, 0],
                                y=dfc.sum()[3:].reset_index().iloc[:, 1],
                                mode='lines',
                                marker={'color': '#a0065a'},
                                name='Confirmed'),
                     go.Scatter(x=dfd.sum()[3:].reset_index().iloc[:, 0],
                                y=dfd.sum()[3:].reset_index().iloc[:, 1],
                                mode='lines',
                                marker={'color': '#6b6c6e'},
                                name='Deceased'),
                     go.Scatter(x=dfr.sum()[3:].reset_index().iloc[:, 0],
                                y=dfr.sum()[3:].reset_index().iloc[:, 1],
                                mode='lines',
                                marker={'color': '#1b63f2'},
                                name='Recovered', )
                     ],
            'layout': go.Layout({
                'xaxis': dict(
                    title='Date'
                ),
                'yaxis': dict(
                    title='Number of people affected'
                ),
                'title': 'Cumulative Cases Confirmed, Deceased and Recovered'
            })
        }
    elif(type=="confirmed"):
        return {
            'data': [go.Scatter(x=dfc.sum()[3:].reset_index().iloc[:,0],
                           y=dfc.sum()[3:].reset_index().iloc[:,1],
                           mode='lines',
                           marker={'color': '#a0065a'},
                           name='Confirmed',
                            text='Confirmed')],
            'layout': go.Layout({
                'xaxis': dict(
                    title='Date'
                ),
                'yaxis': dict(
                    title='Number of people affected'
                ),
                'title': 'Cumulative Confirmed Cases'
            })
        }
    elif(type=="deceased"):
        return {
            'data': [go.Scatter(x=dfd.sum()[3:].reset_index().iloc[:,0],
                           y=dfd.sum()[3:].reset_index().iloc[:,1],
                           mode='lines',
                           marker={'color': '#6b6c6e'},
                           name='Deceased',
                            text='Deceased')],
            'layout': go.Layout({
                'xaxis': dict(
                    title='Date'
                ),
                'yaxis': dict(
                    title='Number of people affected'
                ),
                'title': 'Cumulative Number of people deceased'
            })
        }
    else:
        return {
            'data': [go.Scatter(x=dfr.sum()[3:].reset_index().iloc[:,0],
                           y=dfr.sum()[3:].reset_index().iloc[:,1],
                           mode='lines',
                           marker={'color': '#1b63f2'},
                           name='Recovered',
                            text='Recovered')],
            'layout': go.Layout({
                'xaxis': dict(
                    title='Date'
                ),
                'yaxis': dict(
                    title='Number of people affected'
                ),
                'title': 'Cumulative Number of people recovered'
            })
        }

# @app.callback(Output('Cases','figure'), [Input('picker','value')])
# def update_graph(type):
#
#     if type=='all':
#         tracec= go.Scatter(x=dfc.sum()[3:].reset_index().iloc[:,0],
#                            y=dfc.sum()[3:].reset_index().iloc[:,1],
#                            mode='lines',
#                            marker={'color': '#a0065a'},
#                            name='Confirmed')
#
#         traced= go.Scatter(x=dfd.sum()[3:].reset_index().iloc[:,0],
#                            y=dfd.sum()[3:].reset_index().iloc[:,1],
#                            mode='lines',
#                            marker={'color': '#6b6c6e'},
#                            name='Deceased')
#
#         tracer= go.Scatter(x=dfr.sum()[3:].reset_index().iloc[:,0],
#                            y=dfr.sum()[3:].reset_index().iloc[:,1],
#                            mode='lines',
#                            marker={'color': '#1b63f2'},
#                            name='Recovered',)
#         return {'data':[tracec,traced,tracer], 'layout':go.Layout(title='Cumulative Number of Confirmed, Deceased and Recovered Cases',
#                            xaxis={'title': 'Date'},
#                            yaxis={'title': 'Number of People affected'})}
#     if type=='confirmed':
#         return {'data':go.Scatter(x=dfc.sum()[3:].reset_index().iloc[:, 0],
#                    y=dfc.sum()[3:].reset_index().iloc[:, 1],
#                    mode='lines',
#                    marker={'color': '#a0065a'},
#                    name='Confirmed'),
#                   'layout':go.Layout(title='Cumulative Number of Confirmed, Deceased and Recovered Cases',
#                            xaxis={'title': 'Date'},
#                            yaxis={'title': 'Number of People affected'})}
#     if type == 'deceased':
#         return {'data':go.Scatter(x=dfd.sum()[3:].reset_index().iloc[:,0],
#                            y=dfd.sum()[3:].reset_index().iloc[:,1],
#                            mode='lines',
#                            marker={'color': '#6b6c6e'},
#                            name='Deceased'),
#                 'layout':go.Layout(title='Cumulative Number of Confirmed, Deceased and Recovered Cases',
#                            xaxis={'title': 'Date'},
#                            yaxis={'title': 'Number of People affected'})}
#     if type == 'recovered':
#         return {'data':go.Scatter(x=dfr.sum()[3:].reset_index().iloc[:,0],
#                            y=dfr.sum()[3:].reset_index().iloc[:,1],
#                            mode='lines',
#                            marker={'color': '#1b63f2'},
#                            name='Recovered',),
#                 'layout':go.Layout(title='Cumulative Number of Confirmed, Deceased and Recovered Cases',
#                            xaxis={'title': 'Date'},
#                            yaxis={'title': 'Number of People affected'})}










# traces=[]
    # if 'confirmed' in type:
    #     traces=traces.append(go.Scatter(x=dfc.sum()[3:].reset_index().iloc[:,0],
    #                y=dfc.sum()[3:].reset_index().iloc[:,1],
    #                mode='lines',
    #                marker={'color': '#a0065a'},
    #                name='Confirmed'))
    #
    # if 'deceased' in type:
    #     traces=traces.append(go.Scatter(x=dfd.sum()[3:].reset_index().iloc[:,0],
    #                y=dfd.sum()[3:].reset_index().iloc[:,1],
    #                mode='lines',
    #                marker={'color': '#6b6c6e'},
    #                name='Deceased'))
    #
    # if 'recovered' in type:
    #     traces=traces.append(go.Scatter(x=dfr.sum()[3:].reset_index().iloc[:,0],
    #                y=dfr.sum()[3:].reset_index().iloc[:,1],
    #                mode='lines',
    #                marker={'color': '#1b63f2'},
    #                name='Recovered',))
    # return {'data': traces,
    #         'layout': go.Layout(title='Cumulative Number of Confirmed, Deceased and Recovered Cases',
    #                xaxis={'title': 'Date'},
    #                yaxis={'title': 'Number of People affected'})}

if __name__ == "__main__":
    app.run_server(debug=True)

