# from sentence_transformers import util
# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
from tf_sentence_tr import TFSentenceTransformer
from transformers import AutoTokenizer
import tensorflow as tf


# Hugging Face model id
model_id = 'sentence-transformers/all-MiniLM-L6-v2'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = TFSentenceTransformer(model_id)

sentences = ['\nGOVERNMENT OF INDIA\nJohn Doe\nJAH fafr/ DOB: 12/12/1958\n MALE\n6056 6565 9631\n31 ETTT-ART EH -\n',
             '\nINCOMETAX DEPARTMENT\nGOVT.OF INDIA\nJane Doe\nJoe Braham John\n14/07/1966\n-\nPermanentAccount Number\nADHPB70610\nSignature\n']



# Compute embedding for both lists
# run inference with TFSentenceTransformer
encoded_input_0 = tokenizer(sentences[0], return_tensors="tf")
embedding_0 =  model(encoded_input_0)
encoded_input_1 = tokenizer(sentences[1], return_tensors="tf")
embedding_1 =  model(encoded_input_1)


def docClassification(text):
    encoded_input = tokenizer(text, return_tensors="tf")
    inpEmbedding =  model(encoded_input)
    embeddings = [embedding_0,embedding_1]
    sim = []
    for count, sentence in enumerate(sentences):
        sim.append(tf.keras.losses.cosine_similarity(
            inpEmbedding, embeddings[count]))
    if (sim.index(min(sim)) == 0):
        return 1
    else:
        return 0
