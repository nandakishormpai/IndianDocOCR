import os
import random
import string
import json


def get_name():
    # XXXXX XXXXXXX XX
    name_words = random.choice([2, 3])
    name = ""
    for i in range(0, name_words):
        name += ''.join(random.choices(string.ascii_uppercase,
                                       k=random.choice([3, 4, 5, 6])))
        name += " "
    return name.strip()


def get_fathers_name():
    # XXXX XXX XXXXX
    name_words = random.choice([2, 3])
    name = ""
    for i in range(0, name_words):
        name += ''.join(random.choices(string.ascii_uppercase,
                                       k=random.choice([3, 4, 5, 6])))
        name += " "
    return name.strip()


def get_pan_number():
    # ABCDE1234F
    pan_0_4 = ''.join(random.choices(string.ascii_uppercase,
                                     k=5))
    pan_5_8 = str(random.randint(1001, 9999))
    pan_9 = ''.join(random.choices(string.ascii_uppercase,
                                   k=1))
    pan_number = ''.join([pan_0_4, pan_5_8, pan_9])
    return pan_number


def get_dob():
    # XX/XX/XXXX
    dd = str(random.randint(1, 31)).zfill(2)
    mm = str(random.randint(1, 12)).zfill(2)
    yyyy = str(random.randint(1970, 2003))
    delimeter = random.choice(["/", "-"])
    date = delimeter.join([dd, mm, yyyy])
    return date


def generate_pan(text):
    name = get_name()
    fathers_name = get_fathers_name()
    pan_number = get_pan_number()
    dob = get_dob()

    entities = dict()
    entities["docType"] = "PAN CARD"
    entities["name"] = name
    entities["fathers_name"] = fathers_name
    entities["pan_number"] = pan_number
    entities["dob"] = dob

    text = text.replace("insert_name", name)
    text = text.replace("insert_fathers_name", fathers_name)
    text = text.replace("insert_pan_number", pan_number)
    text = text.replace("insert_dob", dob)

    return (text, entities)


if __name__ == "__main__":
    inp_texts = os.listdir(os.path.join("original", "ocrs"))
    output_texts_dir = os.path.join("generated", "ocrs")
    output_entities_dir = os.path.join("generated", "entities")
    for count, inp_text_file_path in enumerate(inp_texts):
        inp_text_file = open(os.path.join(
            "original", "ocrs", inp_text_file_path), "r")
        inp_text = inp_text_file.read()
        for i in range(0, 4):
            (out_text, out_entities) = generate_pan(inp_text)
            out_text_file = open(os.path.join(
                output_texts_dir, "generated_pan_"+str(count*4 + i).zfill(3)+".txt"), "w")
            out_text_file.write(out_text)
            out_text_file.close()
            with open(os.path.join(
                    output_entities_dir, "generated_pan_entities_"+str(count*4 + i).zfill(3)+".json"), 'w') as json_file:
                json.dump(out_entities, json_file)

        inp_text_file.close()
