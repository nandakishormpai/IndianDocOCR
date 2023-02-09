import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")
headFile = open("promptHead.txt", "r")
promptHead = headFile.read()
footFile = open("promptFoot.txt", "r")
promptFoot = footFile.read()


def ner_pan(OCRtext):
    prompt = "\n".join([promptHead, OCRtext, promptFoot])
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.8,
        presence_penalty=0
    )
    results = (response.choices[0].text).split("\n")
    enitities = dict()
    for result in results:
        if (len(result) >= 3):
            keyVal = result.split(":")
            enitities[keyVal[0].strip()] = keyVal[1].strip()
    with open('entities.json', 'w') as json_file:
        json.dump(enitities, json_file)
    return enitities


if __name__ == "__main__":
    ocrFile = open("OCRtext.txt", "r")
    OCRtext = ocrFile.read()
    ner_pan(OCRtext)
    print(ner_pan(OCRtext))
