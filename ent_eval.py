from stteval.eval_entities.eval_entities import (
    pseudo_recall,
    pseudo_precision,
    f1_score,
)
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

#my_wd = "/home/danae/Documents/BNC projects/STTevaluator/"
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
genfast_tokens = tokenize(genfast_clean)  # change for tokenize_lemmatize
referen_tokens = tokenize(referen_clean)
genesys_tokens_ = tokenize(genesys_clean)
genesys_tokens = clean_genesys_tokens(genesys_tokens_)

# numeric entities
numb_ents = read_entity(my_wd + "data/number_entities.txt")

recall_nuance_genfast = pseudo_recall(referen_tokens, genfast_tokens, numb_ents) # 0.92
recall_nuance_genesys = pseudo_recall(referen_tokens, genesys_tokens, numb_ents) # 0.90

df["recall_genfast"] = recall_nuance_genfast[4]
df["recall_genesys"] = recall_nuance_genesys[4]

precis_nuance_genfast = pseudo_precision(referen_tokens, genfast_tokens, numb_ents)
precis_nuance_genesys = pseudo_precision(referen_tokens, genesys_tokens_, numb_ents)

df["precision_genfast"] = precis_nuance_genfast[4]
df["precision_genesys"] = precis_nuance_genesys[4]

df["number_ref_list"] = recall_nuance_genfast[3]
df.columns

# add the numbers from the reference
number_ref_list = recall_nuance_genfast[3]
numeric_entities = [True if list else False for list in number_ref_list]
df_numbers = df[numeric_entities]
df_numbers.shape

df_numbers = df_numbers[
    [
        "contact_id",
        "file_id",
        "reference",
        "number_ref_list",
        "nuance",
        "recall_genfast",
        "precision_genfast",
        "genesys",
        "recall_genesys",
        "precision_genesys",
    ]
]

df_numbers.to_excel(my_wd + "output/numbers_nuance_vs_genesys.xlsx", index=False)

f1_score_genfast = f1_score(precis_nuance_genfast[5], recall_nuance_genfast[5])
f1_score_genfast = f1_score(precis_nuance_genesys[5], recall_nuance_genesys[5])

df_examples = df_numbers.loc[df["precision_genfast"] - df["precision_genesys"] > 0.7]
df_examples.shape

df_examples.loc[:,'precision_genesys']
df_examples.loc[144,'reference']
df_examples.loc[144,'number_ref_list']
df_examples.loc[144,'nuance']
df_examples.loc[144,'genesys']