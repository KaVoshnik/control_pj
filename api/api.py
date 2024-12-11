import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import time

app = Flask(__name__)

def get_dotabuff_data(account_id):
    url = f"https://www.dotabuff.com/players/{account_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        #  Извлечение даты и времени последнего матча (нужно настроить селекторы под реальную структуру сайта)
        try:
            last_match_time_element = soup.select_one('.data-time-ago')  # ЗАМЕНИТЕ селектор
            last_match_time = last_match_time_element.text.strip() if last_match_time_element else None
            print(last_match_time)
        except AttributeError:
            last_match_time = None


        # Извлечение доли побед (нужно настроить селекторы под реальную структуру сайта)
        try:
            winrate_element = soup.select_one('.winrate') #ЗАМЕНИТЕ селектор
            winrate = winrate_element.text.strip() if winrate_element else None
        except AttributeError:
            winrate = None


        # Извлечение истории последних 5 матчей (нужно настроить селекторы под реальную структуру сайта)
        recent_matches = []
        match_rows = soup.select('.match-list-row')[:5] #ЗАМЕНИТЕ селектор, ограничение на 5 последних матчей
        for row in match_rows:
            try:
                hero_name = row.select_one('.hero-name').text.strip() #ЗАМЕНИТЕ селектор
                match_result = row.select_one('.match-result').text.strip() #ЗАМЕНИТЕ селектор
                game_mode = row.select_one('.game-mode').text.strip() #ЗАМЕНИТЕ селектор
                match_duration = row.select_one('.match-duration').text.strip() #ЗАМЕНИТЕ селектор
                kda = row.select_one('.kda').text.strip() #ЗАМЕНИТЕ селектор
                recent_matches.append({
                    'hero': hero_name,
                    'result': match_result,
                    'game_mode': game_mode,
                    'duration': match_duration,
                    'kda': kda,
                })
            except AttributeError:
                pass


        return {
            'last_match_time': last_match_time,
            'winrate': winrate,
            'recent_matches': recent_matches,
        }
    except requests.exceptions.RequestException as e:
        return {'error': f"Ошибка при запросе: {e}"}
    except Exception as e:
        return {'error': f"Произошла ошибка: {e}"}

@app.route('/api/<account_id>')
def get_data(account_id):
    data = get_dotabuff_data(account_id)
    time.sleep(1)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)