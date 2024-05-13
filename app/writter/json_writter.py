import json


class JSONFileWriter:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def write_in_json_file(self, data: list) -> None:
        serialized_data = [item.to_dict() for item in data]
        with open(self.file_name + ".json", "w", encoding="utf-8") as file:
            json.dump(serialized_data, file, indent=4)
