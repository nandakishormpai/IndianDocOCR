# Code to test out various models, workflows etc

from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import cv2
from PIL import Image

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-handwritten")


image = Image.open("test.jpg").convert("RGB")

pixel_values = processor(image, return_tensors="pt").pixel_values
generated_ids = model.generate(pixel_values)

generated_text = processor.batch_decode(
    generated_ids, skip_special_tokens=True)[0]

print(generated_text)
