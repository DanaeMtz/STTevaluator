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

#my_wd = "/home/danae/Documents/BNC projects/STTevaluator/"
my_wd = "C:/Users/mard019/Desktop/Documents/Git/STTevaluator/"

reference_num = read_reference(
    cols=["Transcription corrigée", "Contact ID"],
    path=my_wd + "data/ref_corpus_numbers.csv",
    enc="utf-8"
)

genfast = read_nuance_trans(path=my_wd + "data/genfast.csv")
genesys = read_genesys_trans(path=my_wd + "data/genesys.csv")

# merge transcriptions
transcriptions = pd.merge(genfast, genesys, on=["file_id", "contact_id"], how="inner")

df_num = pd.merge(transcriptions, reference_num, on=["contact_id"], how="inner")
df_num.dropna(inplace=True)
errors = read_entity(my_wd + "data/errors.txt")
df_num = df_num[~df_num["file_id"].isin(errors)]
df_num.shape

# preprocessing
nuance_trans_num = df_num.loc[:, "nuance"].tolist()
genesys_trans_num = df_num.loc[:, "genesys"].tolist()
referen_trans_num = df_num.loc[:, "reference"].tolist()

nuance_clean_num = nuance_preprocessing(nuance_trans_num)
genesys_clean_num = genesys_preprocessing(genesys_trans_num)
referen_clean_num = reference_preprocessing(referen_trans_num)

# tokenization
nuance_tokens_num = tokenize(nuance_clean_num)
genesys_tokens_num = tokenize(genesys_clean_num)
genesys_tokens_num = clean_genesys_tokens(genesys_tokens_num)
referen_tokens_num = tokenize(referen_clean_num)

# numeric entities
numb_ents = read_entity(my_wd + "data/number_entities.txt")

recall_nuance_num = pseudo_recall(referen_tokens_num, nuance_tokens_num, numb_ents)
recall_genesys_num = pseudo_recall(referen_tokens_num, genesys_tokens_num, numb_ents)

df_num["recall_nuance"] = recall_nuance_num[4]
df_num["recall_genesys"] = recall_genesys_num[4]

df_num["numers_ref_list"] = recall_nuance_num[3]

precis_nuance_num = pseudo_precision(referen_tokens_num, nuance_tokens_num, numb_ents)
precis_genesys_num = pseudo_precision(referen_tokens_num, genesys_tokens_num, numb_ents)

df_num["precision_nuance"] = precis_nuance_num[4]
df_num["precision_genesys"] = precis_genesys_num[4]

f1_score_nuance = f1_score(precis_nuance_num[5], recall_nuance_num[5])
f1_score_genesys = f1_score(precis_genesys_num[5], recall_genesys_num[5])

df_num.to_excel(my_wd + "output/numbers_only_nuance_vs_genesys.xlsx", index=False)

df_examples = df_num.loc[df_num["precision_genesys"]-df_num["precision_nuance"] > 0.2]
df_examples.shape
df_examples.columns
df_examples.loc[:,'precision_genesys']
df_examples.loc[44,'reference']
df_examples.loc[44,'numers_ref_list']
df_examples.loc[44,'nuance']
df_examples.loc[44,'genesys']