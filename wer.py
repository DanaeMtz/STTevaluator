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
    clean_genesys_tokens,
)
import pandas as pd

my_wd = "/home/danae/Documents/BNC projects/STTevaluator/"

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
genfast_tokens = tokenize(genfast_clean)  # change for tokenize_lemmatize
referen_tokens = tokenize(referen_clean)
genesys_tokens_ = tokenize(genesys_clean)
genesys_tokens = clean_genesys_tokens(genesys_tokens_)

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

df_examples = df.loc[df["wer_genesys"] - df["wer_genfast"] > 0.2]
