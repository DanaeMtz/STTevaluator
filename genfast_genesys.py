from stteval.read_data.read_data import (
    read_reference,
    read_nuance_trans,
    read_genesys_trans,
)
import pandas as pd

# read data
#my_wd = "/home/danae/Documents/BNC projects/STTevaluator/"
my_wd = "C:/Users/mard019/Desktop/Documents/Git/STTevaluator/"
reference = read_reference(
    cols=["Transcription corrigée", "Contact ID"],
    path=my_wd + "data/references.csv",
)
genfast = read_nuance_trans(path=my_wd + "data/genfast.csv")
genesys = read_genesys_trans(path=my_wd + "data/genesys.csv")

# merge transcriptions
transcriptions = pd.merge(genfast, genesys, on=['file_id', 'contact_id'], how="left")

df = pd.merge(transcriptions, reference, on=["contact_id"], how="left")
df.dropna(inplace=True)

# preprocessing
genfast_trans = df.loc[:, "nuance"].tolist()
genesys_trans = df.loc[:, "genesys"].tolist()
ref_trans = df.loc[:, "reference"].tolist()

from stteval.preprocessing.preprocessing import nuance_preprocessing, reference_preprocessing, genesys_preprocessing, tokenize_lemmatize, tokenize

genfast_clean = nuance_preprocessing(genfast_trans)
referen_clean = reference_preprocessing(ref_trans)
genesys_clean = genesys_preprocessing(genesys_trans)

print(genfast_trans[10])
print(genfast_clean[10])

print(referen_clean[9])
print(genfast_clean[0])

print(genesys_trans[9])
print(genesys_clean[9])

# tokenization

genfast_tokens, genfast_lem_sents = tokenize_lemmatize(genfast_clean)
referen_tokens, referen_lem_sents = tokenize_lemmatize(referen_clean)
genesys_tokens, genesys_lem_sents = tokenize_lemmatize(genesys_clean)

print(genfast_tokens[9])
print(referen_tokens[9])

print(genesys_tokens[9])




import num2words
import re

iteration = []
for number in range(25):
    iteration.append(num2words.num2words(number + 1, lang="fr"))
    iteration = [re.sub(r"-", " ", sentence) for sentence in iteration]

print(iteration)

iter_tokens = tokenize(iteration)
print(iter_tokens)
flat_list = [item for sublist in iter_tokens for item in sublist]
print(flat_list)
flat_list = list(dict.fromkeys(flat_list))
print(flat_list)


#TODO: function to take the first three tokens of each transcript and compare them with the list tokens associated to numbers 

genesys_tokens[25]

new_transcription = []

flat_list_ = [x for x in flat_list if x != 'et']


for transcription in genesys_tokens:
    if (transcription[0] in flat_list) and (transcription[1] in flat_list) and (transcription[2] in flat_list_) :
        #print(transcription[:3])
        transcription = transcription[3:]
        #print(transcription)
    elif (transcription[0] in flat_list) and (transcription[1] in flat_list):
        #print(transcription[:2])
        transcription = transcription[2:]
        #print(transcription)
    elif (transcription[0] in flat_list or transcription[0] ==' '):
        #print(transcription[:1])
        transcription = transcription[1:]
        #print(transcription)
    else: 
        transcription = transcription
    new_transcription.append(transcription)


new_transcription[3]

