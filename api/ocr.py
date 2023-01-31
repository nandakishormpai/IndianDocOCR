import numpy as np
from doctr.models import ocr_predictor
from doctr.io import DocumentFile

# import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Let's pick the desired backend
os.environ['USE_TF'] = '1'
# os.environ['USE_TORCH'] = '1'

predictor = ocr_predictor(det_arch='linknet_resnet18_rotation',
                          reco_arch='crnn_vgg16_bn', pretrained=True, assume_straight_pages=False)


def ocr_image(img):
    result = predictor([img])
    json_result = result.export()
    words = list()
    for count, block in enumerate(json_result["pages"][0]["blocks"]):
        for lineCount, line in enumerate(block["lines"]):
            for wordCount, word in enumerate(line["words"]):
                if (word["confidence"] > 0.8 and word["value"].isalnum() == True):
                    words.append(word["value"])
    return words


if __name__ == "__main__":
    img = DocumentFile.from_images("IMG PATH")
    result = predictor(np.array(img))
    json_result = result.export()
    words = []
    for count, block in enumerate(json_result["pages"][0]["blocks"]):
        for lineCount, line in enumerate(block["lines"]):
            for wordCount, word in enumerate(line["words"]):
                if (word["confidence"] > 0.8):
                    words.append(word["value"])

    print(words)
