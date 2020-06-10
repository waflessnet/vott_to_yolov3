import glob
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
from shutil import copyfile

from typing_extensions import TypedDict


class Box(TypedDict):
    height: float
    width: float
    left: float
    top: float


class Point(TypedDict):
    x: float
    y: float


class Vott:
    asset: Dict
    regions: List
    version: str

    def __init__(self, dictionary: Dict):
        for key in dictionary:
            setattr(self, key, dictionary[key])


class DarkNet:
    x: float
    y: float
    w: float
    y: float
    label: str
    name_file: str

    def __init__(self, data: Tuple[str, str, float, float, float, float]):
        self.name_file = data[0]
        self.label = data[1]
        self.x = data[2]
        self.y = data[3]
        self.w = data[4]
        self.h = data[5]

    def __str__(self):
        return '{:.6f} {:.6f} {:.6f} {:.6f}\n'.format(self.x, self.y, self.w, self.h)


class Files:

    @staticmethod
    def get_list(_path: str, ext='*.jpg') -> List[str]:
        return glob.glob('{}/{}'.format(_path, ext))

    @staticmethod
    def save_label(_path: str = '', p: int = None, dark: DarkNet = None):
        with open(_path, 'w') as f:
            f.write('{} {}'.format(p, dark))

    @staticmethod
    def save_img(src, dst):
        copyfile(src, dst)

    @staticmethod
    def save_train(_path: str = '', path_img: str = ''):
        with open(_path, 'a') as f:
            f.write('{}\n'.format(path_img))

    @staticmethod
    def save_names(_path: str = '', labels: List[str] = []):
        for l in labels:
            with open(_path, 'a') as f:
                f.write('{}\n'.format(l))

    @staticmethod
    def create_directory(dirs: List[str]):
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)


class Convert:

    @classmethod
    def convert_vott_darknet(cls, path_file: str) -> [DarkNet, None]:
        with open(path_file) as json_content:
            data = Vott(json.load(json_content))
            return DarkNet(cls._relative(data))

    @staticmethod
    def _relative(data: Vott) -> Tuple[str, str, float, float, float, float]:
        full_w = data.asset['size']['width']
        full_h = data.asset['size']['height']

        abs_x = data.regions[0]['boundingBox']['left']
        abs_y = data.regions[0]['boundingBox']['top']

        abs_w = data.regions[0]['boundingBox']['width']
        abs_h = data.regions[0]['boundingBox']['height']

        relative_center_x = float((abs_x + abs_w / 2) / full_w)
        relative_center_y = float((abs_y + abs_h / 2) / full_h)
        relative_width = float(abs_w / full_w)
        relative_height = float(abs_h / full_h)

        label: str = data.regions[0]['tags'][0]
        label = re.sub(r'[\s+-]', '', label)
        name_file: str = data.asset['name']
        return name_file, label, relative_center_x, relative_center_y, relative_width, relative_height
