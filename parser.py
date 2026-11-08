import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://reshutka.ru"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def parse_reshutka():
    print("Начинаем скачивание текстовой структуры с сайта Решутка...")
    gdz_data = {"база_данных": "Текстовая копия Решутка", "предметы": []}

    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        if response.status_code != 200:
            print(f"Ошибка доступа к сайту: код {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        
        for link in links[:50]:
            text = link.text.strip()
            href = link.get('href')
            if href and ('klass' in href or 'gdz' in href):
                gdz_data["предметы"].append({
                    "название": text,
                    "ссылка": BASE_URL + href if href.startswith('/') else href
                })

        with open("database.json", "w", encoding="utf-8") as f:
            json.dump(gdz_data, f, ensure_ascii=False, indent=4)

        print("\n[УСПЕХ] Текстовая структура успешно скопирована в файл database.json!")

    except Exception as e:
        print(f"Произошла ошибка при копировании: {e}")

if __name__ == "__main__":