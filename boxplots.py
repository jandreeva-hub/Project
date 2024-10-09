import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math


# визуализация 'Распределение категориальных данных'
def deals1_category_distribution(Deals1, Quality_mapping):

# Объединение Deals1 с Quality_mapping для получения описаний
    Deals1 = Deals1.merge(Quality_mapping[['Quality_code', 'Description']], how='left', left_on='Quality_code', right_on='Quality_code')

# Определение столбцов для построения графиков
    columns_to_plot = ['Description', 'Stage', 'Source', 'Product', 'Level of Deutsch']

# Исключение значения 'UNKNOWN' для 'Level of Deutsch'
    Deals1_filtered = Deals1[Deals1['Level of Deutsch'] != 'UNKNOWN']

# Установка стиля для графиков
    sns.set(style="whitegrid")

# Определение количества строк и столбцов для графиков
    n_columns = 2  # количество столбцов в сетке подграфиков
    n_rows = math.ceil(len(columns_to_plot) / n_columns)  # количество строк в сетке подграфиков

# Создание подграфиков для каждого столбца
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_columns, figsize=(15, 12))

    axes = axes.flatten()

    fig.suptitle('Распределение категориальных данных', fontsize=16)

    for i, column in enumerate(columns_to_plot):
        if column in Deals1_filtered.columns:
        # Сортировка значений по убыванию частоты
            order = Deals1_filtered[column].value_counts().index
            sns.countplot(data=Deals1_filtered, x=column, ax=axes[i], order=order, palette='viridis')
            axes[i].set_title(f'Распределение {column}')
        
        # Настройка осей
            axes[i].set_xlabel('')
            axes[i].set_ylabel('Количество')
            axes[i].tick_params(axis='x', rotation=45)


    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.savefig('deals1_category_distribution.png')

    plt.show()

def combined_boxplots(Deals1, Calls, Spend):
# Создание боксплотов для числовых данных Deals1
    fig = plt.figure(figsize=(15, 12)) 

# Боксплот для 'Initial Amount Paid'
    plt.subplot(3, 2, 1)
    plt.boxplot([Deals1['Initial Amount Paid'].dropna()], patch_artist=True, labels=['Initial Amount Paid'])
    plt.title('Первый взнос')
    plt.grid(True)

# Боксплот для 'Offer Total Amount'
    plt.subplot(3, 2, 5)
    plt.boxplot(Deals1['Offer Total Amount'].dropna(), patch_artist=True)
    plt.title('Общая сумма предложения')
    plt.grid(True)

# Боксплот для 'Call Duration (in seconds)'
    plt.subplot(3, 2, 2)
    plt.boxplot(Calls['Call Duration (in seconds)'], patch_artist=True)
    plt.title('Продолжительность звонков')
    plt.grid(True)

# Боксплот для 'Spend'
    plt.subplot(3, 2, 3)
    plt.boxplot(Spend['Spend'].dropna(), patch_artist=True)
    plt.title('Расходы на рекламу')
    plt.grid(True)

# Боксплот для 'Impressions' и 'Clicks'
    plt.subplot(3, 2, 4)
    plt.boxplot([Spend['Impressions'].dropna(), Spend['Clicks'].dropna()], patch_artist=True, labels=['Impressions', 'Clicks'])
    plt.title('Распределение показов и кликов')
    plt.grid(True)

    fig.suptitle('Распределение числовых данных', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('combined_boxplots.png')
    plt.show()

Deals1 = pd.read_excel('Deals1.xlsx')
Calls = pd.read_excel('Calls.xlsx')
Spend = pd.read_excel('Spend.xlsx')
Quality_mapping = pd.read_excel('Quality_mapping.xlsx') 

deals1_category_distribution(Deals1, Quality_mapping)
combined_boxplots(Deals1, Calls, Spend)
