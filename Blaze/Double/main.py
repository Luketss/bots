import time
import json
from datetime import datetime

import requests


class Double:
    def __init__(
        self,
        min_pages=2,
        start_date="2023-02-07",
        end_date="2023-03-09",
        save_file=False,
    ):
        self.min_pages = min_pages
        self.start_date = start_date
        self.end_date = end_date
        self.cur_hour = self.get_current_time_hours()
        self.url = f"https://blaze-4.com/api/roulette_games/history?startDate={self.start_date}T{self.cur_hour}.369Z&endDate={self.end_date}T{self.cur_hour}.370Z&page=1"
        self.save_file = save_file
        self.data = self.get_blaze_data()
        self.total = self.get_total_pages()

    def get_current_time_hours(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def get_total_pages(self):
        return self.data["total_pages"]

    def get_blaze_data(self):
        r = requests.get(self.url)

        if self.save_file:
            self.save_data_to_file(r.text)
        return json.loads(r.text)

    def save_data_to_file(self, data):
        with open("result.json", "w") as f:
            f.write(data)

    def get_only_result_data(self):
        results = []
        # print(self.data)
        for v in self.data["records"]:
            val = v["roll"]
            results.append(val)
        print(results)


if __name__ == "__main__":
    obj = Double(save_file=True)
    obj.get_only_result_data()
