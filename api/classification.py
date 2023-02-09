# from sentence_transformers import util
# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
from tf_sentence_tr import TFSentenceTransformer
from transformers import AutoTokenizer
import tensorflow as tf


# Hugging Face model id
model_id = 'sentence-transformers/all-MiniLM-L6-v2'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = TFSentenceTransformer(model_id)


sentences = ['\nGOVERNMENT OF INDIA\nJohn Doe\nJAH fafr/ DOB: 11/11/1998\n MALE\n6126 6234 9531\n31 ETTT-ART EH -\n',
             '\nLERIE\n2186 4544 2121\nFemale\n15/11/1995 DOB: He\nJane Doe\na\nGovernment\n',
             '\nINCOMETAX DEPARTMENT\nGOVT.OF INDIA\nJane Doe\nJoe Braham John\n04/10/1976\n-\nPermanentAccount Number\nADGHT70610\nSignature\n',
             'Signature\n2\nANPRM2537J\nE\n-\nermanent\nJohn Doe\nJoe Braham John\nGOVT.\nDEPARTMENT INCOMETAX\n']


# Compute embedding for both lists
# run inference with TFSentenceTransformer
embeddings = []
for sentence in sentences:
    encoded_input = tokenizer(
        (sentence.replace("\n", " ")).strip(), return_tensors="tf")
    embeddings.append(model(encoded_input))


def docClassification(text):
    encoded_input = tokenizer(
        (text.replace("\n", " ")).strip(), return_tensors="tf")
    inpEmbedding = model(encoded_input)
    sim = []
    for count, embedding in enumerate(embeddings):
        sim.append(tf.keras.losses.cosine_similarity(
            inpEmbedding, embedding))
    print(sim)
    return sim.index(min(sim))
