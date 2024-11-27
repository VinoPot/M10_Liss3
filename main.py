import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser

# Функция для получения координат города, названия валюты, страны и региона
def get_city_info():
    global lat, lng
    city_name = entry.get()
    if not city_name:
        messagebox.showerror("Ошибка", "Пожалуйста, введите название города")
        return

    api_key = '8930e3084cf54b809c283f798c08c8b0'  # ключ пока открытый ,но можно и через переменную окружения, далее модуль os
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}'

    try:
        response = requests.get(url)
        data = response.json()

        if data['results']:
            result = data['results'][0]
            lat = result['geometry']['lat']
            lng = result['geometry']['lng']
            currency_name = result['annotations']['currency']['name']
            country = result['components']['country']
            region = result['components'].get('state', 'Неизвестно')

            result_label.config(text=f"Координаты: {lat}, {lng}\nВалюта: {currency_name}\nСтрана: {country}\nРегион: {region}")
        else:
            messagebox.showerror("Ошибка", "Город не найден")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

# Функция для очистки поля ввода и результатов поиска
def clear_fields():
    entry.delete(0, tk.END)
    result_label.config(text="")

# Функция для открытия карты в браузере
def show_on_map():
    if 'lat' in globals() and 'lng' in globals():
        map_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
        webbrowser.open(map_url)
    else:
        messagebox.showerror("Ошибка", "Сначала выполните поиск города")

# Создание основного окна
root = tk.Tk()
root.title("Координаты городов")

# Создание поля ввода
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Создание кнопки для поиска
search_button = tk.Button(root, text="Поиск", command=get_city_info)
search_button.pack(pady=5)

# Создание кнопки для очистки
clear_button = tk.Button(root, text="Очистить", command=clear_fields)
clear_button.pack(pady=5)

# Создание кнопки для показа на карте
map_button = tk.Button(root, text="Показать на карте", command=show_on_map)
map_button.pack(pady=5)

# Создание метки для отображения результатов
result_label = tk.Label(root, text="", wraplength=300)
result_label.pack(pady=10)

# Запуск основного цикла
root.mainloop()