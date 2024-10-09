import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

deals_data = pd.read_excel('Deals1.xlsx')
spend_data = pd.read_excel('Spend.xlsx')

# Фильтр успешных сделок
successful_deals = deals_data[deals_data['Stage'] == 'Payment Done']

# Объединение данных
successful_deals_with_spend = pd.merge(successful_deals, spend_data, left_on='Source', right_on='Source', how='left')

# Группировка данных
ad_performance = successful_deals_with_spend.groupby('Source').agg(
    total_successful_deals=('Id', 'count'),
    total_spend=('Spend', 'sum'),
    average_deal_value=('Offer Total Amount', 'mean')
).reset_index()

# Сортировка данных по убыванию total_successful_deals
ad_performance = ad_performance.sort_values(by='total_successful_deals', ascending=False)

# Расчет CAC
ad_performance['CAC_per_source'] = ad_performance['total_spend'] / ad_performance['total_successful_deals']

# Юнит-экономика
total_revenue = ad_performance['average_deal_value'].sum()
total_customers = ad_performance['total_successful_deals'].sum()
total_spend = ad_performance['total_spend'].sum()
arpu = total_revenue / total_customers
cac = total_spend / total_customers
ltv = arpu

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Layout приложения
app.layout = html.Div([
    html.H1("Аналитика рекламы: Юнит-экономика и точки роста", 
            style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Кнопка с изображением для управления аудио
    html.Div([
        html.Img(
            src='/assets/free-icon-speaker-2572200.png',  # изображение
            id='play-audio-button',
            style={'width': '50px', 'height': '50px', 'cursor': 'pointer'}
        ),
        
        html.Audio(
            id='audio-player',
            src='/assets/dashboard.mp4',  # аудиофайл
            controls=True,  # контролы для управления
            style={'display': 'none'}  # плеер скрыт по умолчанию
        )
    ], style={'textAlign': 'left', 'marginBottom': '20px'}),

    # Dropdown для выбора метрики
    html.Div([
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Total Successful Deals', 'value': 'total_successful_deals'},
                {'label': 'Total Spend', 'value': 'total_spend'},
                {'label': 'CAC per Source', 'value': 'CAC_per_source'}
            ],
            value='total_successful_deals',
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        ),
    ], style={'marginBottom': '20px'}),

    # График с метриками
    html.Div([
        dcc.Graph(id='combined-chart'),
    ], style={'marginBottom': '20px'}),

    # Вывод юнит-экономики
    html.Div([
        html.H3("Юнит-экономика по продуктам", style={'textAlign': 'center', 'marginBottom': '10px'}),
        html.Div(f"Средний доход на пользователя (ARPU): {arpu:.2f}", style={'textAlign': 'center'}),
        html.Div(f"Стоимость привлечения клиента (CAC): {cac:.2f}", style={'textAlign': 'center'}),
        html.Div(f"Средний жизненный цикл клиента (LTV): {ltv:.2f}", style={'textAlign': 'center'}),
        html.Div("**Точки роста бизнеса**: Увеличение вложений в Facebook Ads и оптимизация креативов в Google Ads приведет к росту ARPU и снижению CAC.", style={'textAlign': 'center'}),
    ], style={'textAlign': 'center', 'marginTop': '30px', 'marginBottom': '30px'}),

    # Иерархия метрик (Sunburst Graph)
    html.Div([
        html.H3("Иерархическое дерево метрик бизнеса с подсветкой точек роста", style={'textAlign': 'center'}),
        dcc.Graph(figure=px.sunburst(
            names=['Business Metrics', 'ARPU', 'CAC', 'LTV', 'Revenue', 'Customers', 'Spend', 'New Customers', 'Retention'],
            parents=['', 'Business Metrics', 'Business Metrics', 'Business Metrics', 'ARPU', 'ARPU', 'CAC', 'CAC', 'LTV'],
            values=[10, 4, 3, 3, 5, 5, 5, 2, 3],
            color_discrete_map={'ARPU': 'green', 'CAC': 'green', 'LTV': 'lightblue', 'Revenue': 'lightgray', 'Customers': 'lightgray', 'Spend': 'lightgray', 'New Customers': 'lightgray', 'Retention': 'lightgray'}
        )),
    ], style={'marginBottom': '30px'}),

    # Гипотезы и решения
    html.Div([
        html.H3("Гипотезы и решения", style={'textAlign': 'center'}),
        html.P("1. Оптимизация таргетинга в Facebook Ads увеличит конверсию на 10%, снизив CAC.", style={'textAlign': 'center'}),
        html.P("2. Улучшение креативов для Google Ads приведет к снижению CAC на 15%.", style={'textAlign': 'center'}),
        html.P("3. Перераспределение бюджета от менее эффективных каналов (CRM, Webinar) к более успешным (Facebook Ads, Google Ads) увеличит общую маржу.", style={'textAlign': 'center'}),
    ], style={'textAlign': 'center', 'marginTop': '30px'}),
    
    # Выводы и рекомендации
    html.Div([
        html.H3("Выводы и рекомендации", style={'textAlign': 'center'}),
        html.P("Рекомендуется оптимизировать вложения в наиболее эффективные рекламные каналы, такие как Facebook Ads и Google Ads, для увеличения ARPU и снижения CAC.", style={'textAlign': 'center'}),
        html.P("Необходимо провести A/B тестирование для проверки гипотез по оптимизации креативов и таргетинга в этих каналах.", style={'textAlign': 'center'}),
    ], style={'textAlign': 'center', 'marginTop': '30px'})
])

# Callback для отображения и воспроизведения аудио
@app.callback(
    Output('audio-player', 'style'),
    Input('play-audio-button', 'n_clicks'),
    prevent_initial_call=True
)
def play_audio(n_clicks):
    if n_clicks:
        return {'display': 'block'}  # вызов аудиоплеера при клике
    return {'display': 'none'}

# Callback для обновления графика
@app.callback(
    Output('combined-chart', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_dashboard(selected_metric):
    # Сортировка данных по убыванию по выбранной метрике
    sorted_data = ad_performance.sort_values(by=selected_metric, ascending=False)

    bar_fig = go.Bar(x=sorted_data['Source'], y=sorted_data[selected_metric], name=selected_metric)
    line_fig = go.Scatter(x=sorted_data['Source'], y=sorted_data['total_spend'], 
                          mode='lines+markers', name='Total Spend', yaxis='y2')

    fig = go.Figure([bar_fig, line_fig])
    fig.update_layout(
        title=f'{selected_metric} и Total Spend по рекламным источникам',
        xaxis_title='Source',
        yaxis_title=selected_metric,
        yaxis2=dict(title='Total Spend', overlaying='y', side='right'),
        legend=dict(x=0, y=-0.2, orientation="h"),
        height=600
    )
    return fig

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)






