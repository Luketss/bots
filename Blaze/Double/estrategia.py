import time
import json
from datetime import datetime

import requests


def get_blaze_data(self):
    r = requests.get(self.url)

    if self.save_file:
        self.save_data_to_file(r.text)
    self.set_data(json.loads(r.text))
    return json.loads(r.text)


def make_request(start_date="2023-03-14", end_date="2023-03-15", save_file=True):
    cur_hour = get_current_time_hours()
    print(cur_hour)
    url = f"https://blaze-4.com/api/roulette_games/history?startDate={start_date}T{cur_hour}.000Z&endDate={end_date}T{cur_hour}.000Z&page=1"

    r = requests.get(url)
    if save_file:
        save_data_to_file(r.text)
    return json.loads(r.text)


def save_data_to_file(data):
    with open("result.json", "w") as f:
        f.write(data)


def get_current_time_hours():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def get_total_pages(data):
    return data["total_pages"]


def get_only_result_data(data):
    results = []
    for i, v in enumerate(data["records"]):
        val = v["color"]
        if i < 5:
            results.append(val)
    return results


def estrategia(result_array):
    color_count = 0
    last = None
    print(result_array)
    for color in result_array:
        if last == None:
            last = color
        if color == last:
            color_count += 1

        else:
            return color_count
    return color_count


if __name__ == "__main__":
    while True:
        data = make_request()
        result = get_only_result_data(data)
        r_est = estrategia(result)
        if r_est == 5:
            print("Entrada válida - 5 resultados da mesma cor")
        elif r_est >= 3:
            print("Possível entrada em breve")
        time.sleep(31)
