import pandas as pd

Calls = pd.read_excel(
    'Calls_in.xlsx',
    dtype={
        'Id': 'str',            
        'CONTACT ID':'str',
        },
    parse_dates=['Call Start Date',
        'Call Start Time'
        ]
)
Calls = Calls.drop_duplicates()

# Удаление строк, где значения в столбцах 'Call Type', 'Call Duration (in seconds)' и 'CONTACT ID' пустые
Calls = Calls.dropna(subset=['Call Type', 'CONTACT ID', 'Call Duration (in seconds)'])
Calls = Calls[(Calls['Call Type'] != '') & (Calls['CONTACT ID'] != '')]

# Удаление ненужных столбцов
Calls = Calls.drop(columns=['Dialled Number','Outgoing Call Status', 'Scheduled in CRM', 'Tag'])

Calls['Call Duration (in seconds)'] = pd.to_numeric(Calls['Call Duration (in seconds)'], errors='coerce')
Calls.to_excel('Calls.xlsx', index=False) 
print(Calls.dtypes)


