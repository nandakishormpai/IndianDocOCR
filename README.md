# IndianDocOCR

## Flask Web APP For Demo in api/ 

```
pip install requirements.txt
python main.py
```
### Website

Head over to http://127.0.0.1:5000/ in your browser for testing.


### API

You can send API requests to http://127.0.0.1:5000/api with <br>
Base64 String of image as value and "image" as key inside the body.

```
{
    "image":"/9j/4AAQSkZJRgABAQEAeAB4AAD/4REQRXhpZgAATU0AKgAAAA...."
}
```

#### Response
```
{
    "result": [
        "Gayatri",
        "2621",
        "Female",
        "HC",
        "Singh",
        "4644",
        "Government",
        "2086"
    ]
}
```



