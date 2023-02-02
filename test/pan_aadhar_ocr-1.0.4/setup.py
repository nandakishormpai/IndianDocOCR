from setuptools import setup

setup(
    name='pan_aadhar_ocr',
    packages=['pan_aadhar_ocr'],
    include_package_data=True,
    version='1.0.4',
    license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    description='Extract information from the pan and aadhar card image',
    long_description=open('README.md').read(),	
    long_description_content_type="text/markdown",
    author='Sanket Gadge',
    author_email='gadgesanket75@gmail.com',
    url='https://github.com/sanket-eazr/Pan-Aadhaar-OCR-With-API',
    download_url='https://github.com/sanket-eazr/Pan-Aadhaar-OCR-With-API.git',
    keywords=['ocr', 'optical character recognition', 'deep learning', 'neural network'],
    install_requires=[
    	"regex==2020.10.15",
	"pytesseract==0.3.7",
	"easyocr==1.2.4",
    ],
)
