from typing import Union, List
from fastapi import (
    FastAPI, 
    File, 
    UploadFile, 
    Response, 
    status
)
import tensorflow as tf

app = FastAPI()

@app.get("/")
def read_root():
    return "Hello world!"

@app.post("/predicts")
async def predicts(images: List[UploadFile], response: Response):

    # Check MIME Type make sure that file is image
    for image in images:
        if image.content_type not in ('image/jpeg', 'image/png'):
            response.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            return { 'message' : 'Just can receive image file type'}
    
    # === GET INPUT ===
    input_tensors = []

    for i, image in enumerate(images):
        # Get image data from body request
        tmp = tf.io.decode_image(
            await image.read(),
            channels=3,
            dtype=tf.dtypes.uint8,
            expand_animations=False
        )

        tmp = tf.image.resize(tmp, size=(224, 224), method='nearest')
        input_tensors.append(tmp)

    input_tensors = tf.convert_to_tensor(input_tensors, dtype=tf.float32)

    # TODO: Preprocessing image into approriate format and size
    # TODO: pass preprocessing result into model
    # TODO: return json (key: result, val: prediction probability)
    return {"filenames": [image.filename for image in images]}
    # return 
# from typing import Annotated

# from fastapi import FastAPI, File, UploadFile

# app = FastAPI()


# @app.post("/files/")
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}
# from fastapi import FastAPI, File, UploadFile
# from typing import List

# app = FastAPI()

# @app.post("/uploadfiles/")
# async def upload_files(files: List[UploadFile]):
#     return {"filenames": [file.filename for file in files]}
