#Географический анализ

import pandas as pd
import folium
from geopy.geocoders import Nominatim
import time
import matplotlib.pyplot as plt
import seaborn as sns


Deals1 = pd.read_excel('Deals1.xlsx')
Level_of_Deutsch_mapping = pd.read_excel('Level_of_Deutsch_mapping.xlsx') 

filtered_deals = Deals1[(Deals1['Stage'] == 'Payment Done') & (Deals1['City'] != 'UNKNOWN')]

# Подсчет количества сделок и определение уровня владения языком для каждого города
grouped_deals = filtered_deals.groupby(['City', 'Level of Deutsch']).agg(
    total_deals=('Id', 'count')
).reset_index()

# получение координат городов
geolocator = Nominatim(user_agent="geoapiExercises")

def get_coordinates(city):
    try:
        location = geolocator.geocode(city)
        time.sleep(1)
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Координаты не найдены для города: {city}")
            return None
    except Exception as e:
        print(f"Ошибка для города {city}: {e}")
        return None

# функция для получения координат
grouped_deals['coordinates'] = grouped_deals['City'].apply(get_coordinates)

# Удаление строк с отсутствующими координатами
grouped_deals = grouped_deals.dropna(subset=['coordinates'])

# Создание карты
m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)

# Определение цветовой схемы на основе уровня владения языком
color_map = {1: "green", 2: "yellow", 3: "orange", 4: "red", 5: "darkred", 6: "purple"}

# Добавление маркеров на карту
for index, row in grouped_deals.iterrows():
    level = row['Level of Deutsch']
    color = color_map.get(level, 'blue')  # Если уровень языка не найден, используем синий цвет
    total_deals = row['total_deals']  # Количество сделок

    # содержимое всплывающего окна
    popup_content = f"<b>City:</b> {row['City']}<br><b>Deals:</b> {total_deals}<br><b>Level:</b> {level}"
    
    # popup для карты
    popup = folium.Popup(html=popup_content, max_width=250)

    # с popup и tooltip
    folium.CircleMarker(
        location=row['coordinates'],
        radius=5 + total_deals / 10,  # Радиус маркера на основе числа сделок
        popup=popup,
        tooltip=f"City: {row['City']} - Deals: {total_deals}, Level: {level}",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)


#file_path = "C:\Users\jandr\Documents\ICH\Python for data analysis\HomeWork\Final_project\germany_map.html"
file_path = "germany_map.html"
m.save(file_path)
print(f"Карта создана и сохранена по пути: {file_path}")


# Построение диаграммы "Распределение сделок по городам (Топ-10) с уровнями владения немецким языком"
# Фильтрация сделок, где этап 'Payment Done', город 'UNKNOWN'
filtered_deals = Deals1[(Deals1['Stage'] == 'Payment Done') & (Deals1['City'] != 'UNKNOWN')]

# Подсчет общего количества сделок по городам и уровням владения немецким языком
city_language_deals = filtered_deals.groupby(['City', 'Level of Deutsch']).agg(
    total_deals=('Id', 'count')  
).reset_index()

# Сортировка по количеству сделок и выбор топ-10 городов
top_10_cities = city_language_deals.groupby('City').agg(
    total_deals=('total_deals', 'sum')
).reset_index().sort_values(by='total_deals', ascending=False).head(10)

# Объединение данных для топ-10 городов с уровнями владения языком
top_10_data = city_language_deals[city_language_deals['City'].isin(top_10_cities['City'])]

# Сортировка данных по убыванию количества сделок в каждой группе по городу
top_10_data['City'] = pd.Categorical(top_10_data['City'], categories=top_10_cities['City'], ordered=True)
top_10_data = top_10_data.sort_values(by=['City', 'total_deals'], ascending=[True, False])

# Построение гистограммы
plt.figure(figsize=(12, 6))
sns.barplot(x='City', y='total_deals', hue='Level of Deutsch', data=top_10_data, palette='Set2')

plt.title('Распределение сделок по городам (Топ-10) с уровнями владения немецким языком')
plt.xlabel('Города')
plt.ylabel('Количество сделок')
plt.xticks(rotation=45)
plt.legend(title='Уровень владения немецким языком')

plt.tight_layout()
plt.savefig("top_10_city_deals_sorted.png")
plt.show()


