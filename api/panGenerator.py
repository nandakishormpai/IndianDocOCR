import json

preName = "Acprlle fOHTST\nPAH ACPrE\nINCOMETAX DEPARTMENT\nGOVT.OF INDIA"
prePanNo = "Permanent Account Number"
end = "Signature"


def generate(data):
    pan = "\n".join([preName, data["name"], data["fathersName"],
                    data["dob"], prePanNo, data["panNo"], end])
    file = open("generatedOCR.txt", "w")
    file.write(pan)
    file.close()


if __name__ == "__main__":
    f = open('PAN_entities.json')
    data = json.load(f)
    generate(data)
