from starlette.responses import FileResponse
import shutil
import uuid


def get_download(type: str, collection: str):
    output_filename = '/tmp/' + str(uuid.uuid4())
    input_dir = '/data/' + type

    if len(collection) > 1 and collection != "default":
        input_dir += '-' + collection

    shutil.make_archive(output_filename, 'zip', input_dir)

    return FileResponse(output_filename + '.zip', media_type='application/x-zip-compressed', filename='export.zip')
