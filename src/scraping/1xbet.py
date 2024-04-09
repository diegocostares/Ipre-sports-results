import json
import re
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone

import requests


class BaseScraper(ABC):
    USER_AGENT = (
        "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36"
    )

    def __init__(self, rate_limit=1.4, filename="resultados.json"):
        self.start_time = time.time()
        self.rate_limit = rate_limit
        self.data_collected = []
        self.filename = filename

    def fetch(self, url):
        time.sleep(self.rate_limit)
        response = requests.get(url, headers={"User-Agent": self.USER_AGENT})
        response.raise_for_status()
        return response.json()

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data_collected, f, ensure_ascii=False, indent=4)

    @abstractmethod
    def generate_urls(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def __del__(self):
        end_time = time.time()
        print(f"Tiempo total de ejecución: {end_time - self.start_time} segundos.")
        print(f"Total de elementos guardados: {len(self.data_collected)}.")


class OneXBetScraper(BaseScraper):
    def __init__(self, num_intervals=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_intervals = num_intervals
        self.run()

    def generate_urls(self):
        current_time = datetime.now(timezone.utc)
        base_time = current_time.replace(hour=2, minute=59, second=59, microsecond=0)# - timedelta(days=1)
        urls_and_dates = []

        for i in range(self.num_intervals):
            date_from = base_time - timedelta(days=i + 1)
            date_to = base_time - timedelta(days=i)
            print(f"{date_from} - {date_to}")
            start_timestamp = int(date_from.timestamp())
            end_timestamp = int(date_to.timestamp())
            url = f"https://1xbet.com/service-api/result/web/api/v1/champs?sportIds=1&dateFrom={start_timestamp}&dateTo={end_timestamp}&lng=en"
            urls_and_dates.append((url, start_timestamp, end_timestamp))

        return urls_and_dates

    @staticmethod
    def extract_stat_values(field_value):
        """Extrae los valores total, del primer tiempo y del segundo tiempo de un campo estadístico."""

        # Intenta encontrar un patrón con cuatro conjuntos de números
        multi_match_4 = re.search(r"(\d+:\d+)\s*\((\d+:\d+),(\d+:\d+),(\d+:\d+),(\d+:\d+)\)", field_value)
        if multi_match_4:
            # Recalcular el total basado en los dos primeros tiempos
            first_half = multi_match_4.group(2)
            second_half = multi_match_4.group(3)
            total_goals_first_half = sum(map(int, first_half.split(":")))
            total_goals_second_half = sum(map(int, second_half.split(":")))
            recalculated_total = f"{total_goals_first_half}:{total_goals_second_half}"
            return {
                "total": recalculated_total,
                "first_time": first_half,
                "second_time": second_half,
            }
        # Intenta encontrar un patrón con múltiples conjuntos de números
        multi_match = re.search(r"(\d+:\d+)\s*\((\d+:\d+),(\d+:\d+)", field_value)
        if multi_match:
            return {
                "total": multi_match.group(1),
                "first_time": multi_match.group(2),
                "second_time": multi_match.group(3),
            }

        # Intenta encontrar un patrón con un solo conjunto de números
        # "0:1 (0:1)" o ""0:0 (0:0)
        single_match = re.search(r"(\d+:\d+)\s*\((\d+:\d+)\)", field_value)
        if single_match:
            return {
                "total": single_match.group(1),
                "first_time": single_match.group(2),
                "second_time": single_match.group(2),
            }

        # Caso base: solo hay un total sin detalles de tiempos
        base_match = re.match(r"(\d+:\d+)", field_value)
        if base_match:
            return {
                "total": base_match.group(1),
                "first_time": base_match.group(1),
                "second_time": base_match.group(1),
            }

        # Si no coincide con ningún patrón, imprime un error y devuelve un diccionario vacío
        print(f"Fallo match para: '{field_value}'")
        return {"total": "", "first_time": "", "second_time": ""}


    def process_stat_fields(self, item, processed_item):
        for sub_game in item.get("subGame", []):
            title = sub_game["title"].replace(" ", "").replace("'", "")
            score = sub_game["score"]
            if title in [
                "Corners",
                "YellowCards",
                "ShotsOnTarget",
                "Offsides",
                "Fouls",
                "Goalkicks",
                "Throw-ins",
            ]:
                stat_values = self.extract_stat_values(score)
                processed_item[f"{title}_total"] = stat_values["total"]
                processed_item[f"{title}_first_time"] = stat_values["first_time"]
                processed_item[f"{title}_second_time"] = stat_values["second_time"]
            elif title == "Playersstats" or title == "DuelbetweenPlayers(Goals)":
                pass
            else:
                processed_item[title] = score

        if "score" in item:
            score_values = self.extract_stat_values(item["score"])
            processed_item["score_total"] = score_values["total"]
            processed_item["score_first_time"] = score_values["first_time"]
            processed_item["score_second_time"] = score_values["second_time"]

        # stat_fields = [
        #     "Corners",
        #     "YellowCards",
        #     "ShotsOnTarget",
        #     "Offsides",
        #     "Fouls",
        #     "Goalkicks",
        #     "Throw-ins",
        # ]

        # for field in stat_fields:
        #     # Este paso es necesario solo si los campos pueden estar también directamente en `item` o necesitan ser recalculados
        #     if field in processed_item and f"{field}_total" not in processed_item:
        #         stat_values = self.extract_stat_values(processed_item[field])
        #         processed_item[f"{field}_total"] = stat_values["total"]
        #         processed_item[f"{field}_first_time"] = stat_values["first_time"]
        #         processed_item[f"{field}_second_time"] = stat_values["second_time"]


    def process_game_data(self, game_data):
        processed_data = []
        for item in game_data.get("items", []):
            processed_item = {
                k: item[k]
                for k in item
                if k
                not in [
                    "opp1Images",
                    "opp2Images",
                    "opp1Ids",
                    "opp2Ids",
                    "count",
                    "subGame",
                    "hasSubGame",
                    "countSubGame",
                    "matchInfos",  # items generales
                    # Los campos estadísticos se procesarán por separado
                    "score",
                    "Corners",
                    "YellowCards",
                    "ShotsOnTarget",
                    "Offsides",
                    "Fouls",
                    "Goalkicks",
                    "Throw-ins",
                ]
            }
            # Procesar matchInfos utilizando un método dedicado
            self.process_match_infos(item, processed_item)

            # Procesar campos estadísticos
            self.process_stat_fields(item, processed_item)

            # Convertir el timestamp 'dateStart' en fecha y hora separadas de manera segura
            if "dateStart" in item:
                date_start_obj = datetime.fromtimestamp(item["dateStart"], timezone.utc)
                processed_item["date"] = date_start_obj.strftime("%Y-%m-%d")
                processed_item["time"] = date_start_obj.strftime("%H:%M UTC")

            processed_data.append(processed_item)

        return processed_data

    def process_match_infos(self, item, processed_item):
        match_info_mapping = {
            "1": "round",
            "2": "stadium",
            "7": "city",
            "9": "temperature",
            "11": "country",
            "20": "uv_index",  # eso o sensacion Sensación
            "21": "weather_condition",
            "22": "wind_m_s",
            "23": "unknown23",
            "24": "wind",
            "25": "match_id",
            "26": "pressure",
            "27": "humidity_percentage",
            "28": "humidity",
            "35": "precipitation_probability",
            "36": "precipitation",
        }

        match_infos = item.get("matchInfos", {})
        for key, value in match_infos.items():
            mapped_key = match_info_mapping.get(key, key)
            processed_item[mapped_key] = value

    def fetch_games(self, champ_id, date_from, date_to):
        games_url = f"https://1xbet.com/service-api/result/web/api/v1/games?champId={champ_id}&dateFrom={date_from}&dateTo={date_to}&lng=en"
        game_data = self.fetch(games_url)
        return self.process_game_data(game_data)

    def run(self):
        urls_and_dates = self.generate_urls()
        with ThreadPoolExecutor() as executor:
            future_to_url = {
                executor.submit(self.fetch, url): (url, date_from, date_to)
                for url, date_from, date_to in urls_and_dates
            }

            for future in as_completed(future_to_url):
                url, date_from, date_to = future_to_url[future]
                data = future.result()
                if data:
                    games_futures = [
                        executor.submit(self.fetch_games, item["id"], date_from, date_to)
                        for item in data.get("items", [])
                    ]

                    for game_future in as_completed(games_futures):
                        processed_game_data = game_future.result()
                        if processed_game_data:
                            self.data_collected.extend(processed_game_data)  # Añadir datos procesados

        self.save_data()


if __name__ == "__main__":
    OneXBetScraper(num_intervals=1)
