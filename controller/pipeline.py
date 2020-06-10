from __future__ import annotations
from abc import ABC, abstractmethod
from logging import Handler
from typing import Optional, List

from controller.images import Files, Convert

PATH_SAVE_IMAGES = 'train/images'
PATH_SAVE_LABELS = 'train/labels'
PATH_SAVE_TRAIN = 'train/train.txt'
PATH_SAVE_CLASS = 'train/custom.names'
PATH_SAVE_DATA = 'train/train.data'


class RequestHandler:
    path_json = None
    path_image = None
    path_output = None
    path_labels = None
    save_train = None
    save_names = None
    labels: List[str] = []
    json_files: List[str] = []
    images_files: List[str] = []

    def __init__(self, path_json: str, path_image: str, path_output: str):
        self.path_output = path_output
        self.path_image = path_image
        self.path_json = path_json


class Handler(ABC):

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[None]:
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: RequestHandler) -> None:
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class GetFiles(AbstractHandler):
    def handle(self, request: RequestHandler) -> None:
        request.json_files = Files.get_list(request.path_json, '*.json')
        request.images_files = Files.get_list(request.path_image, '*.jpg')
        dirs = [
            '{}/{}'.format(request.path_output, PATH_SAVE_IMAGES),
            '{}/{}'.format(request.path_output, PATH_SAVE_LABELS)
        ]
        Files.create_directory(dirs)
        super().handle(request)


class VottToDarknet(AbstractHandler):
    def handle(self, request: RequestHandler) -> None:
        labels = []
        save_train = '{}/{}'.format(request.path_output, PATH_SAVE_TRAIN)
        save_names = '{}/{}'.format(request.path_output, PATH_SAVE_CLASS)
        request.save_train = save_train
        request.save_names = save_names
        for j in request.json_files:
            dark = Convert.convert_vott_darknet(j)
            lb_path = '{}/{}/{}'.format(request.path_output, PATH_SAVE_LABELS, dark.name_file.replace('.jpg', '.txt'))
            img_path = '{}/{}/{}'.format(request.path_output, PATH_SAVE_IMAGES, dark.name_file)
            org_img_path = '{}/{}'.format(request.path_image, dark.name_file)

            try:
                p = labels.index(dark.label)
                Files.save_label(_path=lb_path, p=p, dark=dark)
                Files.save_img(org_img_path, img_path)
                Files.save_train(save_train, img_path)

            except ValueError:
                labels.append(dark.label)
                p = labels.index(dark.label)
                Files.save_label(_path=lb_path, p=p, dark=dark)
                Files.save_img(org_img_path, img_path)
                Files.save_train(save_train, img_path)

        Files.save_names(save_names, labels)
        request.labels = labels
        super().handle(request)


class ConfigFile(AbstractHandler):
    def handle(self, request: RequestHandler) -> None:
        classes = len(request.labels)
        train = request.save_train
        names = request.save_names
        save_data = '{}/{}'.format(request.path_output, PATH_SAVE_DATA)
        content_file = "classes={classes}\n" \
                       "train={train}\n" \
                       "valid=\n" \
                       "names={names}".format(classes=classes, train=train, names=names)

        print(content_file)
        with open(save_data, 'w') as f:
            f.write(content_file)
