import json
import os
from src.processing import Sharp, Resize, Halftone
from pepeline import read, save
from tqdm.contrib.concurrent import process_map
from os import cpu_count

PROCESSED_TYPE_DICT = {
    "sharp": Sharp,
    "resize": Resize,
    "screentone": Halftone
}


class ParProcess:
    def __init__(self, input_file: str):
        with open(input_file, "r") as f:
            data = json.load(f)
        self.input_folder = data.get("in_folder", "test/INPUT")
        self.output_folder = data.get("out_folder", "test/OUTPUT")
        processed = data["processed"]
        processed_turn = []
        for dicts in processed:
            process = PROCESSED_TYPE_DICT[dicts["type"]]
            processed_turn.append(process(dicts))
        self.processed_turn = processed_turn
        self.max_workers = data.get("max_workers", min(32, cpu_count() + 4))

    def __folder_exists(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        if not os.path.exists(self.input_folder):
            raise print("Not input folder")

    def __file_list(self) -> list:
        return [
            file
            for file in os.listdir(self.input_folder)
            if os.path.isfile(os.path.join(self.input_folder, file))
        ]

    def process(self, img_name: str):
        img = read(f'{self.input_folder}/{img_name}', 0, 0)
        for process in self.processed_turn:
            img = process.run(img)
        img_basic_name = img_name.split(".")[0]
        save(img, f'{self.output_folder}/{img_basic_name}.png')

    def run(self):
        self.__folder_exists()
        files = self.__file_list()
        process_map(self.process, files, max_workers=self.max_workers)
