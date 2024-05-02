import json
import os
from src.processing import Sharp, Resize, Halftone
from pepeline import read, save
from tqdm.contrib.concurrent import process_map
from tqdm import tqdm
from os import cpu_count

PROCESSED_TYPE_DICT = {
    "sharp": Sharp,
    "resize": Resize,
    "screentone": Halftone
}


class Process:
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
        self.paralel = data.get("paralel")
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
        try:
            img_folder = os.path.join(self.input_folder, img_name)
            img = read(img_folder, 0, 0)
            for process in self.processed_turn:
                img = process.run(img)
            img_basic_name = img_name.split(".")[0] + ".png"
            out_folder = os.path.join(self.output_folder, img_basic_name)
            save(img, out_folder)
        except Exception as e:
            print(e)

    def run(self):
        self.__folder_exists()
        files = self.__file_list()
        if self.paralel:
            process_map(self.process, files, max_workers=self.max_workers)
        else:
            for img_name in tqdm(files):
                self.process(img_name)
