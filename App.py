import pandas   as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

## 1- Cargar data frame
df = pd.read_csv('onlinefoods.csv')

## 2 - Transformación de datos (si es necesario)

## 3 - Crear la aplicación Dash
external_stylesheets = [dbc.themes.CERULEAN]    # Puedes cambiar el tema a tu preferencia
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'reporte de pedidos de comida Online'

## 4 - Crear el layout de la aplicación
app.layout = dbc.Container([
    dbc.Row([html.H1("Reporte de Pedidos de Comida Online")]),
    dbc.Row([
        dbc.Col([
            html.Label("Seleccione el Género:"),
            dcc.Dropdown(
            id='selector_Genero',
            options=[{'label': Genero, 'value': Genero} for Genero in df['Gender'].unique()],
            value=df['Gender'].unique()[0]  # Valor por defecto
        )
        ],width=3),
        dbc.Col([
            html.Label("Seleccione la Ocupación:"),
            dcc.RadioItems(
            id='Selector_ocupacion',
            options=[{'label': ocupacion, 'value': ocupacion} for ocupacion in df['Occupation'].unique()],
            value=df['Occupation'].unique()[0], # Valor por defecto
        )],width=3),
        
        dbc.Col([
            html.Label("Seleccione el Rango de Edad:"),
            dcc.RangeSlider(
            id='selector_edad',
            min=df['Age'].min(),
            max=df['Age'].max(),
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(df['Age'].min(), df['Age'].max() + 1)},
            step=1
        )],width=6)
        ]),
    dbc.Row([    
        dbc.Col([     
            dcc.Graph(id='grafico_barras')
        ]),
        dbc.Col([
            dcc.Graph(id='grafico_pastel')
        ]),
    ])    
],fluid=True)

## 5 - Crear el callback para actualizar el gráfico
@app.callback(
   [Output('grafico_barras', 'figure'),
    Output('grafico_pastel', 'figure')],
   [Input('Selector_ocupacion', 'value'), 
    Input('selector_Genero', 'value'),
    Input('selector_edad', 'value')]
)

def crear_graficas(valor_ocupacion,valor_genero, valor_edad):
    #filtrar el DataFrame por género seleccionado
    df_filtrado = df[(df['Gender'] == valor_genero) & (df['Occupation'] == valor_ocupacion) & (df['Age'] >= valor_edad[0]) & (df['Age'] <= valor_edad[1])]
    
    Promedio_feedback_estado_civil = df_filtrado.groupby(["Marital Status",'Feedback'])['Age'].mean().reset_index().sort_values(by='Feedback', ascending=False)
    grafico_barras = px.bar(Promedio_feedback_estado_civil, 
                            x='Marital Status', 
                            y='Age',
                            color='Feedback',
                            title='Promedio de Tamaño de Familia por Estado Civil',
                            color_discrete_sequence=['#65c78c','#f74a50'])
    
    Conteo_votos_feedback = df_filtrado.groupby(['Feedback'])['Age'].mean().reset_index().sort_values(by='Feedback', ascending=False)
    grafico_pastel = px.pie(Conteo_votos_feedback,
                            names= 'Feedback',
                            values= 'Age',
                            title='Proporción de Tamaño de Familia por Estado Civil',
                            color_discrete_sequence=['#65c78c','#f74a50'])
    
    return grafico_barras, grafico_pastel
    
