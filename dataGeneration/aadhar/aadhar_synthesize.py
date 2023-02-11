import os
import random
import string
import json


def get_name():
    # Xxxx Xxxxxx Xxx
    name_words = random.choice([2, 3])
    name = ""
    for i in range(0, name_words):
        word = ''.join(random.choices(string.ascii_uppercase,
                                      k=1))
        word += ''.join(random.choices(string.ascii_lowercase,
                                       k=random.choice([3, 4, 5])))
        name += word
        name += " "
    return name.strip()


def get_aadhar_number():
    # 1234 5678 9123
    aadhar_0 = str(random.randint(1001, 9999))
    aadhar_1 = str(random.randint(1, 9999)).zfill(4)
    aadhar_2 = str(random.randint(1, 9999)).zfill(4)
    aadhar_number = ' '.join([aadhar_0, aadhar_1, aadhar_2])
    return aadhar_number


def get_gender():
    gender = random.choice(["Male", "Female", "Transgender"])
    return random.choice([gender, gender.upper()])


def get_dob():
    # XX/XX/XXXX
    dd = str(random.randint(1, 31)).zfill(2)
    mm = str(random.randint(1, 12)).zfill(2)
    yyyy = str(random.randint(1970, 2003))
    delimeter = random.choice(["/", "-"])
    date = delimeter.join([dd, mm, yyyy])
    return date


def get_year():
    return str(random.randint(1970, 2003))


def generate_aadhar(text):
    name = get_name()
    aadhar_number = get_aadhar_number()
    dob = get_dob()
    year = get_year()
    gender = get_gender()

    entities = dict()
    entities["docType"] = "AADHAR CARD"
    entities["name"] = name
    entities["aadhar_number"] = aadhar_number
    entities["gender"] = gender

    text = text.replace("insert_name", name)
    text = text.replace("insert_aadhar_number", aadhar_number)
    text = text.replace("insert_gender", gender)
    if ("insert_dob" in text):
        text = text.replace("insert_dob", dob)
        entities["dob"] = dob
    else:
        text = text.replace("insert_year_of_birth", year)
        entities["year_of_birth"] = year

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
            (out_text, out_entities) = generate_aadhar(inp_text)
            out_text_file = open(os.path.join(
                output_texts_dir, "generated_aadhar_"+str(count*4 + i).zfill(3)+".txt"), "w")
            out_text_file.write(out_text)
            out_text_file.close()
            with open(os.path.join(
                    output_entities_dir, "generated_aadhar_entities_"+str(count*4 + i).zfill(3)+".json"), 'w') as json_file:
                json.dump(out_entities, json_file)

        inp_text_file.close()
