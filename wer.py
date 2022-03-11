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
    verint_preprocessing,
    tokenize,
    tokenize_lemmatize,
    clean_genesys_tokens,
)
import pandas as pd

my_wd = "C:/Users/mard019/Desktop/Documents/Git/STTevaluator/"
#my_wd = "/home/danae/Documents/BNC projects/STTevaluator/"

reference = read_reference(
    cols=["Transcription corrigée", "Contact ID", "Transcription Verint"],
    path=my_wd + "data/references.csv",
)
reference = reference.rename(columns={"Transcription Verint": "verint"})

reference_num = read_reference(
    cols=["Transcription corrigée", "Contact ID"],
    path=my_wd + "data/ref_corpus_numbers.csv",
    enc="utf-8"
)

nuance = read_nuance_trans(path=my_wd + "data/genfast.csv")
genesys = read_genesys_trans(path=my_wd + "data/genesys.csv")

# merge transcriptions
transcriptions = pd.merge(nuance, genesys, on=["file_id", "contact_id"], how="inner")

df = pd.merge(transcriptions, reference, on=["contact_id"], how="inner")
df.dropna(inplace=True)
errors = read_entity(my_wd + "data/errors.txt")
df = df[~df["file_id"].isin(errors)]
df.shape

# preprocessing
nuance_trans = df.loc[:, "nuance"].tolist()
verint_trans = df.loc[:, "verint"].tolist()
genesys_trans = df.loc[:, "genesys"].tolist()
referen_trans = df.loc[:, "reference"].tolist()

nuance_clean = nuance_preprocessing(nuance_trans)
verint_clean = verint_preprocessing(verint_trans)
genesys_clean = genesys_preprocessing(genesys_trans)
referen_clean = reference_preprocessing(referen_trans)

# tokenization
nuance_tokens, nuance_lem_sents = tokenize_lemmatize(nuance_clean)
verint_tokens, verint_lem_sents = tokenize_lemmatize(verint_clean)
genesys_tokens, genesys_lem_sents = tokenize_lemmatize(genesys_clean)
genesys_tokens = clean_genesys_tokens(genesys_tokens)
referen_tokens, referen_lem_sents = tokenize_lemmatize(referen_clean)

# nuance_tokens = tokenize(nuance_clean)
# verint_tokens = tokenize(verint_clean)
# genesys_tokens = tokenize(genesys_clean)
# genesys_tokens = clean_genesys_tokens(genesys_tokens)
# referen_tokens = tokenize(referen_clean)

# nuance_tokens[1]
# verint_tokens[1]
# genesys_tokens[1]
# referen_tokens[1]

# compute WER
# WER for each transcription and compute the global wer for evaluate the whole engin
wer_nuance, global_wer_nuance = compute_wer(referen_tokens, nuance_tokens)
wer_verint, global_wer_verint = compute_wer(referen_tokens, verint_tokens)
wer_genesys, global_wer_genesys = compute_wer(referen_tokens, genesys_tokens)

df["wer_nuance"] = wer_nuance
df["wer_verint"] = wer_verint
df["wer_genesys"] = wer_genesys

df = df[
    [
        "contact_id",
        "file_id",
        "reference",
        "nuance",
        "wer_nuance",
        "verint",
        "wer_verint",
        "genesys",
        "wer_genesys",
    ]
]

df.to_excel(my_wd + "output/WER_nuance_verint_genesys.xlsx", index=False)

df_examples = df.loc[(df["wer_genesys"] - df["wer_nuance"] > 0.2) & (df["wer_verint"] - df["wer_nuance"] > 0.2)]

#df_examples.to_excel(my_wd + "output/WER_genfast_vs_genesys_examples.xlsx", index=False)

df_examples.shape

df_examples.loc[:,'wer_genesys']
df_examples.loc[:,'wer_verint']

df_examples.loc[363,'reference']
df_examples.loc[363,'nuance']
df_examples.loc[363,'genesys']
df_examples.loc[363,'verint']
