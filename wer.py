from stteval.compute_wer.compute_wer import compute_wer
from stteval.read_data.read_data import (
    read_reference,
    read_nuance_trans,
    read_genesys_trans,
    read_entity,
)
from stteval.preprocessing.preprocessing import (
    nuance_preprocessing,
    reference_preprocessing,
    genesys_preprocessing,
    tokenize,
    tokenize_lemmatize, 
    clean_genesys_tokens,
)
import pandas as pd

# my_wd = "/home/danae/Documents/BNC projects/STTevaluator/"
my_wd = "C:/Users/mard019/Desktop/Documents/Git/STTevaluator/"

reference = read_reference(
    cols=["Transcription corrigée", "Contact ID"],
    path=my_wd + "data/references.csv",
)
genfast = read_nuance_trans(path=my_wd + "data/genfast.csv")
genesys = read_genesys_trans(path=my_wd + "data/genesys.csv")

# merge transcriptions
transcriptions = pd.merge(genfast, genesys, on=["file_id", "contact_id"], how="inner")

df = pd.merge(transcriptions, reference, on=["contact_id"], how="inner")
df.dropna(inplace=True)
errors = read_entity(my_wd + "data/errors.txt")
df = df[~df["file_id"].isin(errors)]
df.shape

# preprocessing
genfast_trans = df.loc[:, "nuance"].tolist()
genesys_trans = df.loc[:, "genesys"].tolist()
ref_trans = df.loc[:, "reference"].tolist()

genfast_clean = nuance_preprocessing(genfast_trans)
referen_clean = reference_preprocessing(ref_trans)
genesys_clean = genesys_preprocessing(genesys_trans)

# tokenization
genfast_tokens , genfast_lem_sents =  tokenize_lemmatize(genfast_clean)  # change for tokenize_lemmatize
referen_tokens , referen_lem_sents =  tokenize_lemmatize(referen_clean)
genesys_tokens_, genesys_lem_sents = tokenize_lemmatize(genesys_clean)
genesys_tokens = clean_genesys_tokens(genesys_tokens_)

genfast_tokens[0]
referen_tokens[0]
genesys_tokens[0]

# compute WER
# WER for each transcription and compute the global wer for evaluate the whole engin
wer_genfast, global_wer_genfast = compute_wer(referen_tokens, genfast_tokens)
wer_genesys, global_wer_genesys = compute_wer(referen_tokens, genesys_tokens)

df["wer_genfast"] = wer_genfast
df["wer_genesys"] = wer_genesys

df = df[
    [
        "contact_id",
        "file_id",
        "reference",
        "nuance",
        "wer_genfast",
        "genesys",
        "wer_genesys",
    ]
]

df.to_excel(my_wd + "output/WER_nuancegenfast_vs_genesys.xlsx", index=False)


df_examples = df.loc[df["wer_genesys"] - df["wer_genfast"] > 0.2]

df_examples = df_examples[
    [
        "contact_id", 
        "reference",
        "nuance",
        "wer_genfast",
        "genesys",
        "wer_genesys",
    ]
]

df_examples.to_excel(my_wd + "output/WER_genfast_vs_genesys_examples.xlsx", index=False)

df_examples.shape

df_examples.loc[:,'wer_genesys']
df_examples.loc[716,'reference']
df_examples.loc[143,'nuance']
df_examples.loc[716,'genesys']