import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import pearsonr


# Анализируйте тенденцию создания сделок с течением времени и их связь с звонками.

def calls_deals_week(Calls, Deals1):

# Установка индекса для возможности ресемплинга по времени
    Calls.set_index('Call Start Date', inplace=True)
    Deals1.set_index('Created', inplace=True)

# Агрегация по неделям
    calls_weekly = Calls.resample('W').count()[['Id']]  
    deals_weekly = Deals1.resample('W').count()[['Id']] 

# Объединение данных по звонкам и сделкам на основе общего временного индекса
    merged_weekly = calls_weekly.join(deals_weekly, lsuffix='_calls', rsuffix='_deals', how='inner')

# Вычисление корреляции и p-value
    correlation, p_value = pearsonr(merged_weekly['Id_calls'], merged_weekly['Id_deals'])

    fig, ax = plt.subplots(figsize=(10, 6))

# График для звонков (агрегированные по неделям)
    ax.plot(merged_weekly.index, merged_weekly['Id_calls'], label='Calls', color='blue')

# График для сделок (агрегированные по неделям)
    ax.plot(merged_weekly.index, merged_weekly['Id_deals'], label='Deals', color='green')

    significance_text = 'значимо' if p_value < 0.05 else 'не значимо'
    ax.text(0.05, 0.80, f'p-value: {p_value:.4f} ({significance_text})', transform=ax.transAxes, fontsize=12, verticalalignment='top')

# Настройка осей и заголовка
    ax.set_xlabel('Неделя')
    ax.set_ylabel('Количество')
    ax.set_title('Звонки и сделки по неделям')

    ax.legend(loc='upper left')
    ax.text(0.05, 0.85, f'Коэффициент корреляции: {correlation:.2f}', transform=ax.transAxes, fontsize=12, verticalalignment='top')

    ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.7)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1)) 
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%W')) 
    plt.xticks(rotation=45)

    plt.savefig('calls_deals_week.png')
    plt.show()


#Изучите распределение времени закрытия сделок и продолжительность периода от создания до закрытия.

def weekly_deals_close_distribution(Deals1):
    Deals1 = Deals1.dropna(subset=['Closing Date', 'Created'])

# Расчет продолжительности от создания до закрытия сделки
    Deals1['duration'] = (Deals1['Closing Date'] - Deals1['Created']).dt.days

# Агрегация данных по неделям для количества сделок
    deals_weekly_count = Deals1.resample('W', on='Closing Date').count()

# Агрегация данных по неделям для средней продолжительности (в днях)
    deals_weekly_duration = Deals1.resample('W', on='Closing Date')['duration'].mean()

# Вычисление корреляции между количеством сделок и средней продолжительностью закрытия
    correlation, p_value = pearsonr(deals_weekly_count['Id'], deals_weekly_duration)
    fig, ax1 = plt.subplots(figsize=(10, 6))

# График количества сделок
    ax1.plot(deals_weekly_count.index, deals_weekly_count['Id'], color='darkblue', label='Количество сделок', linewidth=2)
    ax1.set_xlabel('Недели')
    ax1.set_ylabel('Количество сделок', color='darkblue')
    ax1.tick_params(axis='y', labelcolor='darkblue')

# Настройка оси X для отображения недель
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1)) 
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%W'))  
    plt.xticks(rotation=45)

# Вторая ось Y для продолжительности периода от создания до закрытия
    ax2 = ax1.twinx()
    ax2.plot(deals_weekly_duration.index, deals_weekly_duration, color='darkred', label='Средняя продолжительность (дни)', linewidth=2)
    ax2.set_ylabel('Средняя продолжительность (дни)', color='darkred')
    ax2.tick_params(axis='y', labelcolor='darkred')

    plt.title('Количество сделок и средняя продолжительность закрытия по неделям')
    ax1.grid(True, which='major', axis='both', linestyle='--', linewidth=0.7)

    ax1.text(0.05, 0.85, f'Коэффициент корреляции: {correlation:.2f}', transform=ax1.transAxes, fontsize=12, verticalalignment='top')
    significance_text = 'значимо' if p_value < 0.05 else 'не значимо'
    ax1.text(0.05, 0.80, f'p-value: {p_value:.4f} ({significance_text})', transform=ax1.transAxes, fontsize=12, verticalalignment='top')

    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2)
    fig.tight_layout()
    plt.savefig('weekly_deals_close_distribution.png')
    plt.show()

Deals1 = pd.read_excel('Deals1.xlsx')
Calls = pd.read_excel('Calls.xlsx')

calls_deals_week(Calls, Deals1)
weekly_deals_close_distribution(Deals1)


