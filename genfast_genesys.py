from stteval.read_data.read_data import (
    read_reference,
    read_nuance_trans,
    read_genesys_trans,
)
import pandas as pd

# read data
# my_wd = "/home/danae/Documents/BNC projects/STTevaluator/"
my_wd = "C:/Users/mard019/Desktop/Documents/Git/STTevaluator/"
reference = read_reference(
    cols=["Transcription corrigée", "Contact ID"],
    path=my_wd + "data/references.csv",
)
genfast = read_nuance_trans(path=my_wd + "data/genfast.csv")
genesys = read_genesys_trans(path=my_wd + "data/genesys.csv")

# merge transcriptions
transcriptions = pd.merge(genfast, genesys, on=["file_id", "contact_id"], how="left")

df = pd.merge(transcriptions, reference, on=["contact_id"], how="left")
df.dropna(inplace=True)

# preprocessing
genfast_trans = df.loc[:, "nuance"].tolist()
genesys_trans = df.loc[:, "genesys"].tolist()
ref_trans = df.loc[:, "reference"].tolist()

from stteval.preprocessing.preprocessing import (
    nuance_preprocessing,
    reference_preprocessing,
    genesys_preprocessing,
    tokenize_lemmatize,
    tokenize,
    clean_genesys_tokens,
)

genfast_clean = nuance_preprocessing(genfast_trans)
referen_clean = reference_preprocessing(ref_trans)
genesys_clean = genesys_preprocessing(genesys_trans)

# tokenization
genfast_tokens, genfast_lem_sents = tokenize_lemmatize(genfast_clean)
referen_tokens, referen_lem_sents = tokenize_lemmatize(referen_clean)
genesys_tokens, genesys_lem_sents = tokenize_lemmatize(genesys_clean)
genesys_tokens = clean_genesys_tokens(genesys_tokens)

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
df.to_excel(my_wd + "output/WER_nuance_vs_genesys.xlsx", index=False)

