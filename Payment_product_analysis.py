#Анализ платежей и продуктов
import pandas as pd
import matplotlib.pyplot as plt


Deals1 = pd.read_excel('Deals1.xlsx')
Calls = pd.read_excel('Calls.xlsx')
Spend = pd.read_excel('Spend.xlsx')

# Подсчет успешных сделок по типам платежей
payment_analysis = Deals1.groupby('Payment Type').agg({
    'Id': 'count',  # Total deals
    'Stage': lambda x: (x == 'Payment Done').sum()  # Successful deals
}).reset_index()

# Процент успешных сделок для каждого типа платежа
payment_analysis.rename(columns={'Id': 'Total Deals', 'Stage': 'Successful Deals'}, inplace=True)
payment_analysis['Success Rate'] = payment_analysis['Successful Deals'] / payment_analysis['Total Deals']

# Фильтрация для исключения 'UNKNOWN' типа платежа (в верхнем регистре)
payment_analysis = payment_analysis[payment_analysis['Payment Type'] != 'UNKNOWN']

# Сортировка по убыванию по количеству сделок (Total Deals)
payment_analysis = payment_analysis.sort_values(by='Total Deals', ascending=False)

# Построение объединенного графика
fig, ax1 = plt.subplots(figsize=(10, 6))

# Столбчатая диаграмма для общего количества сделок
ax1.bar(payment_analysis['Payment Type'], payment_analysis['Total Deals'], color='skyblue', label='Total Deals')
ax1.set_xlabel('Тип платежа')
ax1.set_ylabel('Всего сделок')
ax1.set_title('Распределение видов платежей и показатель успешности')

# Вторая ось Y для показателя успешности
ax2 = ax1.twinx()
ax2.plot(payment_analysis['Payment Type'], payment_analysis['Success Rate'], color='green', marker='o', label='Success Rate')
ax2.set_ylabel('Показатель успешности')

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.savefig('distribution_success_rate_payment_type.png')
plt.show()





# # Популярность и успешность продуктов и видов образования

bubble_data = Deals1[(Deals1['Stage'] == 'Payment Done') & (Deals1['Product'].notna())]

bubble_grouped = bubble_data.groupby(['Product', 'Education Type']).size().reset_index(name='Count')

plt.figure(figsize=(12, 7))

# построение пузырьковой диаграммы
plt.scatter(bubble_grouped['Product'], bubble_grouped['Education Type'], 
            s=bubble_grouped['Count'] * 20,  # Scale down the bubble size
            alpha=0.6, edgecolors="w", linewidth=2)

# добавление текстовых меток для пузырьков (успешные сделки)
for i in range(len(bubble_grouped)):
    plt.text(bubble_grouped['Product'][i], bubble_grouped['Education Type'][i], 
             str(bubble_grouped['Count'][i]), color='black', ha='center', va='center', fontsize=10)

plt.xlim(-0.5, len(bubble_grouped['Product'].unique()) - 0.5)
plt.ylim(-0.5, len(bubble_grouped['Education Type'].unique()) - 0.5)

plt.title('Успешные сделки для продуктов и типов обучения')
plt.xlabel('Продукт')
plt.ylabel('Тип обучения')
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.savefig('Successful_deals_products_types.png')
plt.show()



