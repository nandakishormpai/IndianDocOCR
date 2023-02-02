# Pan Aadhar OCR
## _Extract Text from Pan and Aadhar Cards_

Pan Aadhar OCR is a python package which takes an Image of a valid Pan/Aadhar
Document and extracts the text from it and returns the information in JSON format.

- Easy to use
- Returns information in JSON
- Works even faster with the GPU
- If you don't have a GPU, you can still run it on CPU, but slower


## Tech
Pan Aadhar OCR uses a number of open source projects to work properly:

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - Ready-to-use OCR with 80+ supported languages and all popular writing scripts including Latin, Chinese, Arabic, Devanagari, Cyrillic and etc.
- [Python](https://www.python.org/) - Python is a programming language that lets you work quickly and integrate systems more effectively.
- [OpenCV](https://opencv.org/) - OpenCV is open source and released under the BSD 3-Clause License. It is free for commercial use.

## Installation

This library requires [Python](https://www.python.org/) 3.6+ to run.
As well as you also need to install tesseract on your system.
If you have Linux based system just run:
```sh
sudo apt install tesseract-ocr
```
On windows system you will need to download Tessaract from [here](https://tesseract-ocr.github.io/tessdoc/Downloads.html). and Add it to the Path.

Install the package.

```sh
pip install pan-aadhar-ocr
```

Then Import the package.

```sh
from pan_aadhar_ocr import Pan_Info_Extractor
```

Create an instance of the extractor.

```sh
extractor = Pan_Info_Extractor()
```

Pass the image to the extractor to get the results.
```sh
extractor.info_extractor('/content/pan test.jpeg')
```

This will return a result as following:
```json
{
    "Pan_number": "EKAPS0276J", 
    "Name": "John Kevin Doe",
    "Father_Name": "Kevin Doe",
    "DOB": "31/10/1992"
} 
```