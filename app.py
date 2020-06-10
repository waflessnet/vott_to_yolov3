from controller.pipeline import GetFiles, VottToDarknet, RequestHandler, ConfigFile

if __name__ == '__main__':
    req = RequestHandler(
        path_json='/home/panchito/Documentos/train/Destino1',
        path_image='/home/panchito/Documentos/train/Destino1/Origen-1-PascalVOC-export/JPEGImages',
        path_output='/tmp/two'
    )
    start = GetFiles()
    start.set_next(VottToDarknet()).set_next(ConfigFile())
    start.handle(req)