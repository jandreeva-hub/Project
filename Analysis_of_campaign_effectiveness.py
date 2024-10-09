import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


Deals1 = pd.read_excel('Deals1.xlsx')
Calls = pd.read_excel('Calls.xlsx')
Spend = pd.read_excel('Spend.xlsx')
#Анализ эффективности кампаний: 

# 1. Сравните эффективность различных кампаний с точки зрения генерации лидов и коэффициента конверсии.

# # Расчет количества лидов, сгенерированных каждым источником
leads_by_source = Deals1.groupby('Source').size().reset_index(name='Leads Generated')
numeric_columns = Spend.select_dtypes(include='number').columns.tolist()

# Объединение с данными о расходах, чтобы получить расходы и клики для каждого источника
source_performance_df = pd.merge(leads_by_source, Spend.groupby('Source')[numeric_columns].sum().reset_index(), on='Source', how='left')

# Расчет коэффициента конверсии и стоимости лида
source_performance_df['Conversion Rate'] = source_performance_df['Leads Generated'] / source_performance_df['Clicks']
source_performance_df['Cost per Lead'] = source_performance_df['Spend'] / source_performance_df['Leads Generated']

# Удаление бесконечных и NaN, полученных в результате деления на ноль.
source_performance_df.replace([float('inf'), -float('inf')], None, inplace=True)
source_performance_df.fillna(0, inplace=True)
source_performance_df = source_performance_df.sort_values(by='Leads Generated', ascending=False)
fig, ax1 = plt.subplots(figsize=(10, 6))

# Столбчатая диаграмма для сгенерированных лидов
ax1.bar(source_performance_df['Source'], source_performance_df['Leads Generated'], color='b', alpha=0.6, label='Leads Generated')
ax1.set_xlabel('Source')
ax1.set_ylabel('Генерированные лиды')
ax1.set_title('Эффективность источника: количество потенциальных клиентов и коэффициент конверсии')
ax1.legend(loc='upper left')

# вторая ось Y для коэффициента конверсии
ax2 = ax1.twinx()
ax2.plot(source_performance_df['Source'], source_performance_df['Conversion Rate'], color='g', marker='o', label='Conversion Rate')
ax2.set_ylabel('Конверсия')
ax2.legend(loc='upper right')

ax1.set_xticklabels(source_performance_df['Source'], rotation=45, ha='right')

plt.savefig('Source_efficiency.png')
plt.show()




# #2. Оцените эффективность различных маркетинговых источников Source) в генерировании качественных лидов.
# Объедининение сделок с данными о расходах, чтобы включить информацию о кампании

deals_campaign_df = pd.merge(Deals1, Spend, on='Source', how='left')

# Расчет количества лидов, полученных в результате каждой кампании
leads_by_campaign = deals_campaign_df.groupby('Campaign').size().reset_index(name='Leads Generated')

# Выбор числовых столбцов из Spend
numeric_columns = Spend.select_dtypes(include='number').columns.tolist()

# Объединение данных о расходах, чтобы получить данные о расходах и кликах для каждой кампании
campaign_performance_df = pd.merge(leads_by_campaign, Spend.groupby('Campaign')[numeric_columns].sum().reset_index(), on='Campaign', how='left')

# Расчет коэффициента конверсии и стоимости лида для каждой кампании
campaign_performance_df['Conversion Rate'] = campaign_performance_df['Leads Generated'] / campaign_performance_df['Clicks']
campaign_performance_df['Cost per Lead'] = campaign_performance_df['Spend'] / campaign_performance_df['Leads Generated']

# Замена бесконечных значений и NaN на 0
campaign_performance_df.replace([float('inf'), -float('inf')], None, inplace=True)
campaign_performance_df.fillna(0, inplace=True)

# Проверка созданного DataFrame
print(campaign_performance_df)
campaign_performance_df = campaign_performance_df.sort_values(by='Leads Generated', ascending=False)
# Извлечение соответствующих метрик для построения графика
campaigns = campaign_performance_df['Campaign']
leads_generated = campaign_performance_df['Leads Generated']
conversion_rate = campaign_performance_df['Conversion Rate']
cost_per_lead = campaign_performance_df['Cost per Lead']

# Построение графика
fig, ax1 = plt.subplots(figsize=(12, 6))

# Столбчатая диаграмма для сгенерированных лидов
ax1.bar(campaigns, leads_generated, color='b', alpha=0.6, label='Leads Generated')
ax1.set_xlabel('Campaign')
ax1.set_ylabel('Генерированные лиды')
ax1.set_title('Эффективность маркетинговой кампании: качественная генерация лидов')
ax1.legend(loc='upper left')

# Вторая ось Y для коэффициента конверсии
ax2 = ax1.twinx()
ax2.plot(campaigns, conversion_rate, color='g', marker='o', label='Conversion Rate')
ax2.set_ylabel('Конверсия')
ax2.legend(loc='upper right')

ax1.set_xticklabels(campaigns, rotation=45, ha='right')
plt.tight_layout() 
plt.savefig('quality_lead_generation.png')
plt.show()
