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
    tokenize_lemmatize,
    tokenize,
    clean_genesys_tokens,
)
from stteval.compute_wer.compute_wer import compute_wer
from stteval.eval_entities.eval_entities import (
    pseudo_recall,
    pseudo_precision,
    f1_score,
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
transcriptions = pd.merge(genfast, genesys, on=["file_id", "contact_id"], how="inner")

df = pd.merge(transcriptions, reference, on=["contact_id"], how="inner")
df.dropna(inplace=True)
errors = read_entity(my_wd + "data/errors.txt")

df = df[~df['file_id'].isin(errors)]
df.shape

# preprocessing
genfast_trans = df.loc[:, "nuance"].tolist()
genesys_trans = df.loc[:, "genesys"].tolist()
ref_trans = df.loc[:, "reference"].tolist()

genfast_clean = nuance_preprocessing(genfast_trans)
referen_clean = reference_preprocessing(ref_trans)
genesys_clean = genesys_preprocessing(genesys_trans)

# compute WER
# tokenization
genfast_tokens, genfast_lem_sents = tokenize_lemmatize(genfast_clean)
referen_tokens, referen_lem_sents = tokenize_lemmatize(referen_clean)
genesys_tokens, genesys_lem_sents = tokenize_lemmatize(genesys_clean)
genesys_tokens_ = clean_genesys_tokens(genesys_tokens)


# WER for each transcription and compute the global wer for evaluate the whole engin
wer_genfast, global_wer_genfast = compute_wer(referen_tokens, genfast_tokens)
wer_genesys, global_wer_genesys = compute_wer(referen_tokens, genesys_tokens_)

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

#df.to_excel(my_wd + "output/WER_nuancegenfast_vs_genesys.xlsx", index=False)

# entity evaluation
# tokenization
genfast_tokens = tokenize(genfast_clean)
referen_tokens = tokenize(referen_clean)
genesys_tokens = tokenize(genesys_clean)
genesys_tokens_ = clean_genesys_tokens(genesys_tokens)

# numeric entities 
numb_ents = read_entity(my_wd + "data/number_entities.txt")


recall_nuance_genfast = pseudo_recall(referen_tokens, genfast_tokens, numb_ents)
recall_nuance_genesys = pseudo_recall(referen_tokens, genesys_tokens_, numb_ents)


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

# banking entities 
bank_ents = read_entity(my_wd + "data/bank_entities.txt")

recall_nuance_genfast = pseudo_recall(referen_tokens, genfast_tokens, bank_ents)
recall_nuance_genesys = pseudo_recall(referen_tokens, genesys_tokens_, bank_ents)

df["recall_genfast"] = recall_nuance_genfast[4]
df["recall_genesys"] = recall_nuance_genesys[4]

precis_nuance_genfast = pseudo_precision(referen_tokens, genfast_tokens, bank_ents)
precis_nuance_genesys = pseudo_precision(referen_tokens, genesys_tokens_, bank_ents)

df["precision_genfast"] = precis_nuance_genfast[4]
df["precision_genesys"] = precis_nuance_genesys[4]

df["banking_ref_list"] = recall_nuance_genfast[3]

f1_score_genfast = f1_score(precis_nuance_genfast[5], recall_nuance_genfast[5])
f1_score_genfast = f1_score(precis_nuance_genesys[5], recall_nuance_genesys[5])

# add the numbers from the reference 
banking_ref_list = recall_nuance_genfast[3]
banking_entities = [True if list else False for list in banking_ref_list]
df_banking = df[banking_entities]
df_banking.shape

df_banking = df_banking[
    [
        "contact_id",
        "file_id",
        "reference",
        "banking_ref_list",
        "nuance",
        "recall_genfast",
        "precision_genfast",
        "genesys",
        "recall_genesys",
        "precision_genesys",
    ]
]

df_banking.to_excel("output/banking_nuance_vs_genesys.xlsx", index=False)
