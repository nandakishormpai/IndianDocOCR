from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import matplotlib.pyplot as plt
import os
os.environ['USE_TORCH'] = '1'


doc = DocumentFile.from_images("test_2.jpg")
predictor = ocr_predictor(pretrained=True)
result = predictor(doc)

print(result)

result.show(doc)
