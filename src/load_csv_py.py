import csv


def load_csv(file_path: str) -> list[list[str]]:
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        data = [row for row in csv_reader]
    return data
