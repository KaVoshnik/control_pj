import requests
import customtkinter as ctk
import json

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def fetch_data():
    account_id = account_id_entry.get()
    try:
        response = requests.get(f"http://127.0.0.1:5000/api/{account_id}")
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            result_label.configure(text=f"Ошибка: {data['error']}")
            winrate_label.configure(text="")
            matches_textbox.delete("1.0", ctk.END)
        else:
            result_label.configure(text=f"Последний матч: {data['last_match_time']}")
            winrate_label.configure(text=f"Winrate: {data['winrate']}")
            matches_textbox.delete("1.0", ctk.END)
            for match in data['recent_matches']:
                matches_textbox.insert(ctk.END, f"Герой: {match['hero']}, Результат: {match['result']}, Режим: {match['game_mode']}, Длительность: {match['duration']}, KDA: {match['kda']}\n")
    except requests.exceptions.RequestException as e:
        result_label.configure(text=f"Ошибка сети: {e}")
    except json.JSONDecodeError:
        result_label.configure(text="Ошибка обработки JSON")
    except Exception as e:
        result_label.configure(text=f"Произошла неизвестная ошибка: {e}")


root = ctk.CTk()
root.geometry("600x400")
root.title("Dotabuff Data Fetcher")

account_id_label = ctk.CTkLabel(master=root, text="Введите ID игрока Dotabuff:")
account_id_label.pack(pady=10, padx=10)

account_id_entry = ctk.CTkEntry(master=root)
account_id_entry.pack(pady=10, padx=10)

fetch_button = ctk.CTkButton(master=root, text="Получить данные", command=fetch_data)
fetch_button.pack(pady=10, padx=10)

result_label = ctk.CTkLabel(master=root, text="")
result_label.pack(pady=5, padx=10)

winrate_label = ctk.CTkLabel(master=root, text="")
winrate_label.pack(pady=5, padx=10)

matches_textbox = ctk.CTkTextbox(master=root, width=400)
matches_textbox.pack(pady=10, padx=10)

root.mainloop()
