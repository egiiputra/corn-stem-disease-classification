import json

from typing import Union, List
from fastapi import (
    FastAPI, 
    File, 
    UploadFile, 
    Response, 
    status
)

from tensorflow import (
    convert_to_tensor,
    uint8, 
    float32
)
from tensorflow.io import decode_image
from tensorflow.image import resize as image_resize
import tensorflow.lite as tflite 


CLASS_NAMES = ['sehat', 'giberella', 'anthracnose']

MODEL_NAME = "vgg16-original-adam"

# Load the TFLite model
interpreter = tflite.Interpreter(model_path=f"models/{MODEL_NAME}.tflite")
interpreter.allocate_tensors()  # Allocate memory for the model

# Get input/output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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

    input_tensors = []

    for i, image in enumerate(images):
        # Get image data from body request
        input_tensor = decode_image(
            await image.read(),
            channels=3,
            dtype=uint8,
            expand_animations=False
        )
        input_tensors.append(input_tensor)

    predictions = []
    for i, input_tensor in enumerate(input_tensors):
        input_tensor = image_resize(input_tensor, size=(224, 224), method='nearest')

        input_tensor = convert_to_tensor([ input_tensor / 255 ], dtype=float32)

        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], input_tensor)
        # Run inference
        interpreter.invoke()
        # Get the output
        output_data = interpreter.get_tensor(output_details[0]['index'])
        output_data = output_data.tolist()
        
        predictions.append({ 
            "file_name": images[i].filename,
            "scores": {clas:output_data[0][i] for i, clas in enumerate(CLASS_NAMES) }
        })

    return {
        "model": MODEL_NAME,
        "predictions": predictions
    }