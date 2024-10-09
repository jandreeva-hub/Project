#Анализ эффективности работы отдела продаж.  

import pandas as pd
import matplotlib.pyplot as plt

Deals1 = pd.read_excel('Deals1.xlsx')
Calls = pd.read_excel('Calls.xlsx')
Spend = pd.read_excel('Spend.xlsx')

# Анализ владельцев сделок и кампаний

# Подсчет общего количества сделок, успешных сделок и общей суммы продаж
owner_campaign_analysis = Deals1.groupby(['Deal Owner Name', 'Source']).agg({
    'Id': 'count',  # всего сделок
    'Stage': lambda x: (x == 'Payment Done').count(),  # успешные сделки
    'Offer Total Amount': 'sum'  # общая сумма продаж
}).reset_index()

# Переименование столбцов
owner_campaign_analysis.rename(columns={'Id': 'Total Deals', 'Stage': 'Successful Deals'}, inplace=True)

# Расчет коэффициента конверсии
owner_campaign_analysis['Conversion Rate'] = owner_campaign_analysis['Successful Deals'] / owner_campaign_analysis['Total Deals']

owner_campaign_analysis = owner_campaign_analysis.sort_values(by='Total Deals', ascending=False)

fig, ax1 = plt.subplots(figsize=(12, 6))

# Построение столбчатой диаграммы для каждого источника
for source in owner_campaign_analysis['Source'].unique():
    subset = owner_campaign_analysis[owner_campaign_analysis['Source'] == source]
    ax1.bar(subset['Deal Owner Name'], subset['Total Deals'], label=source)

ax1.set_xlabel('Владелец сделки')
ax1.set_ylabel('Общее число сделок')
ax1.set_title('Общее число сделок по отношению к владельцам сделок и маркетинговым кампаниям')
ax1.legend(title='Source')

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Deals_Owner_Source.png')
plt.show()
