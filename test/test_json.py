import pytest

from controller.images import Convert, Files
from controller.pipeline import VottToDarknet, RequestHandler


@pytest.mark.parametrize(
    'path_json',
    [
        'testdata/vott.json'
    ]
)
def test_json_test(path_json: str):
    Convert.convert_vott_darknet(path_json)


@pytest.mark.parametrize(
    'path_json, path_img',
    [
        (
                '/home/panchito/Documentos/train/Destino1',
                '/home/panchito/Documentos/train/Destino1/Origen-1-PascalVOC-export/JPEGImages'
        )
    ]
)
def test_v_to_d(path_json: str, path_img: str):
    vott = VottToDarknet()
    req = RequestHandler(
        path_json=path_json,
        path_image=path_img,
        path_output=''
    )
    req.json_files = Files.get_list(path_json, '*.json')
    vott.handle(req)
