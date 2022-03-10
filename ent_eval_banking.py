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
    verint_preprocessing,
    tokenize,
    clean_genesys_tokens,
)
import pandas as pd

#my_wd = "C:/Users/mard019/Desktop/Documents/Git/STTevaluator/"
my_wd = "/home/danae/Documents/BNC projects/STTevaluator/"

reference = read_reference(
    cols=["Transcription corrigée", "Contact ID", "Transcription Verint"],
    path=my_wd + "data/references.csv",
)
reference = reference.rename(columns={"Transcription Verint": "verint"})

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
nuance_trans = df.loc[:, "nuance"].tolist()
verint_trans = df.loc[:, "verint"].tolist()
genesys_trans = df.loc[:, "genesys"].tolist()
referen_trans = df.loc[:, "reference"].tolist()

nuance_clean = nuance_preprocessing(nuance_trans)
verint_clean = verint_preprocessing(verint_trans)
genesys_clean = genesys_preprocessing(genesys_trans)
referen_clean = reference_preprocessing(referen_trans)

# tokenization
nuance_tokens = tokenize(nuance_clean)
verint_tokens = tokenize(verint_clean)
genesys_tokens = tokenize(genesys_clean)
genesys_tokens = clean_genesys_tokens(genesys_tokens)
referen_tokens = tokenize(referen_clean)

# banking entities
bank_ents = read_entity(my_wd + "data/bank_entities.txt")

recall_nuance = pseudo_recall(referen_tokens, nuance_tokens, bank_ents)
recall_verint = pseudo_recall(referen_tokens, verint_tokens, bank_ents)
recall_genesys = pseudo_recall(referen_tokens, genesys_tokens, bank_ents)

df["recall_nuance"] = recall_nuance[4]
df["recall_verint"] = recall_verint[4]
df["recall_genesys"] = recall_genesys[4]

df["banking_ref_list"] = recall_nuance[3]

precis_nuance = pseudo_precision(referen_tokens, nuance_tokens, bank_ents)
precis_verint = pseudo_precision(referen_tokens, verint_tokens, bank_ents)
precis_genesys = pseudo_precision(referen_tokens, genesys_tokens, bank_ents)

df["precision_nuance"] = precis_nuance[4]
df["precision_verint"] = precis_verint[4]
df["precision_genesys"] = precis_genesys[4]

f1_score_nuance = f1_score(precis_nuance[5], recall_nuance[5])
f1_score_verint = f1_score(precis_verint[5], recall_verint[5])
f1_score_genesys = f1_score(precis_genesys[5], recall_genesys[5])

# filter only th sentences with at least one banking word
banking_ref_list = recall_nuance[3]
banking_entities = [True if list else False for list in banking_ref_list]
sum(banking_entities)
df["recall_nuance"].isnull().sum()

df_banking = df[banking_entities]
df_banking.shape

df_banking = df_banking[
    [
        "contact_id",
        "file_id",
        "reference",
        "banking_ref_list",
        "nuance",
        "recall_nuance",
        "precision_nuance",
        "verint",
        "recall_verint",
        "precision_verint",
        "genesys",
        "recall_genesys",
        "precision_genesys",
    ]
]

#df_banking.to_excel("output/banking_nuance_vs_genesys.xlsx", index=False)
df_banking.shape

df_examples = df_banking.loc[df["recall_nuance"] - df["recall_genesys"] > 0.5]
df_examples.shape

df_examples.loc[553,'reference']
df_examples.loc[553,'nuance']
df_examples.loc[553,'genesys']
df_examples.loc[555,'verint']