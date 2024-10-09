import pandas as pd
import numpy as np

# Чтение данных из Excel
Calls = pd.read_excel('Calls.xlsx')
Spend = pd.read_excel('Spend.xlsx')
Deals1 = pd.read_excel('Deals1.xlsx')

# Функция для вычисления описательных статистик, моды и диапазона
def compute_stats(df, columns):
    stats = pd.DataFrame()
    for column in columns:
        if column in df.columns:
            desc_stats = df[column].describe()
            mode = df[column].mode().values[0] if not df[column].mode().empty else np.nan
            range_value = np.ptp(df[column])
            
            column_stats = pd.DataFrame({
                'mean': [desc_stats['mean']],
                'std': [desc_stats['std']],
                'min': [desc_stats['min']],
                '25%': [desc_stats['25%']],
                '50%': [desc_stats['50%']],
                '75%': [desc_stats['75%']],
                'max': [desc_stats['max']],
                'Mode': [mode],
                'Range': [range_value]
            }, index=[column])
            
            stats = pd.concat([stats, column_stats], axis=0)
    return stats

# Вычисление статистики для Calls, Spend и Deals1
Calls_stats = compute_stats(Calls, ['Call Duration (in seconds)'])
Spend_stats = compute_stats(Spend, ['Impressions', 'Spend', 'Clicks'])
Deals1_stats = compute_stats(Deals1, ['Initial Amount Paid', 'Offer Total Amount','SLA_minutes'])

# Добавление категории
Calls_stats['Category'] = 'Calls'
Spend_stats['Category'] = 'Spend'
Deals1_stats['Category'] = 'Deals1'

# Объединение всех статистик
all_stats = pd.concat([Calls_stats, Spend_stats, Deals1_stats], axis=0)

# Перестановка столбцов так, чтобы Category был первым
all_stats = all_stats.reset_index().rename(columns={'index': 'Column'})
all_stats = all_stats[['Category', 'Column', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'Mode', 'Range']]

# Сохранение в Excel
with pd.ExcelWriter('statistics_summary.xlsx') as writer:
    all_stats.to_excel(writer, sheet_name='Summary', index=False)

print("cтатистика сохранена в файл 'statistics_summary.xlsx'")



