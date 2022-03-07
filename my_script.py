# ---# load libraries #---#
from stteval.read_data.read_data import (
    read_reference,
    read_nuance_trans,
    read_amazon_trans,
    read_entity,
)
from stteval.preprocessing.preprocessing import (
    reference_preprocessing,
    nuance_preprocessing,
    amazon_preprocessing,
    tokenize_lemmatize,
)
from stteval.compute_wer.compute_wer import compute_wer
from stteval.eval_entities.eval_entities import (
    pseudo_recall,
    pseudo_precision,
    f1_score,
)
from stteval.preprocessing.preprocessing import tokenize
import pandas as pd
from functools import reduce

# ---# read data #---#
reference = read_reference(
    cols=["Transcription corrigée", "Contact ID"],
    path="/home/danae/Documents/BNC projects/STTevaluator/data/references.csv",
)  # read the reference
nuance_gen       = read_nuance_trans(path="../data/nuance_transcriptions_gen.csv", enc="latin-1")  # read nuance
nuance_genfast   = read_nuance_trans(path="../data/nuance_transcriptions_genfast.csv")             # read nuance
nuance_genfast_p = read_nuance_trans(path="../data/nuance_transcriptions_genfast_plus_c.csv")        # read nuance

nuance_gen = nuance_gen.rename(columns={"nuance": "nuance_gen"})
nuance_genfast = nuance_genfast.rename(columns={"nuance": "nuance_genfast"})
nuance_genfast_p = nuance_genfast_p.rename(columns={"nuance": "nuance_genfast_p"})

amazon = read_amazon_trans(
    path="C:/Users/mard019/Banque Nationale du Canada/Guerlesquin, Valentin - Transcriptions"
)  # read amazon
#transcriptions = pd.merge(
#    nuance, amazon, on=["file_id", "contact_id"], how="inner"
#).drop_duplicates()  # merge transcriptions
dfs = [nuance_genfast_p, amazon] #nuance_gen, nuance_genfast, 
transcriptions = reduce(lambda left, right: pd.merge(left, right, on=["file_id", "contact_id"]), dfs)
df = pd.merge(
    transcriptions, reference, on=["contact_id"], how="left"
)  # merge reference
df.dropna(inplace=True)
df.columns
df.shape
df.head()
# ---# preprocessing #---#
nuance_gen = df.loc[:, "nuance_gen"].tolist()
nuance_genfast = df.loc[:, "nuance_genfast"].tolist()
nuance_genfast_p = df.loc[:, "nuance_genfast_p"].tolist()

amazon = df.loc[:, "amazon"].tolist()
refere = df.loc[:, "reference"].tolist()

nuance_gen_clean = nuance_preprocessing(nuance_gen)
nuance_genfast_clean = nuance_preprocessing(nuance_genfast)
nuance_genfast_p_clean = nuance_preprocessing(nuance_genfast_p)

amazon_clean = amazon_preprocessing(amazon)
refere_clean = reference_preprocessing(refere)

# ---# tokenization #---#
nuance_gen_tokens, nuance_lem_sents = tokenize_lemmatize(nuance_gen_clean)
nuance_genfast_tokens, nuance_lem_sents = tokenize_lemmatize(nuance_genfast_clean)
nuance_genfast_p_tokens, nuance_lem_sents = tokenize_lemmatize(nuance_genfast_p_clean)

amazon_tokens, amazon_lem_sents = tokenize_lemmatize(amazon_clean)
refere_tokens, refere_lem_sents = tokenize_lemmatize(refere_clean)

# ---# compute wer #---#
wer_nuance_gen,       global_wer_nuance_gen       = compute_wer(refere_tokens, nuance_gen_tokens)
wer_nuance_genfast,   global_wer_nuance_genfast   = compute_wer(refere_tokens, nuance_genfast_tokens)
wer_nuance_genfast_p, global_wer_nuance_genfast_p = compute_wer(refere_tokens, nuance_genfast_p_tokens)
wer_amazon, global_wer_amazon = compute_wer(refere_tokens, amazon_tokens)

df["wer_nuance_gen"] = wer_nuance_gen
df["wer_nuance_genfast"] = wer_nuance_genfast
df["wer_nuance_genfast_p"] = wer_nuance_genfast_p
df["wer_amazon"] = wer_amazon

df = df[
    [
        "contact_id",
        "file_id",
        "reference",
        "nuance_gen",
        "wer_nuance_gen",
        "nuance_genfast", 
        "wer_nuance_genfast",
        "nuance_genfast_p", 
        "wer_nuance_genfast_p",
        "amazon",
        "wer_amazon",
    ]
]
df.to_excel("../../results/WER_nuance_vs_amazon.xlsx", index=False)

# ---# entity evaluation #---#
numb_ents = read_entity("../data/number_entities.txt")

nuance_gen_tokens = tokenize(nuance_gen_clean)
nuance_genfast_tokens = tokenize(nuance_genfast_clean)
nuance_genfast_p_tokens = tokenize(nuance_genfast_p_clean)
amazon_tokens = tokenize(amazon_clean)
refere_tokens = tokenize(refere_clean)

# ---# numeric entities #---#
# recall
recall_nuance_gen       = pseudo_recall(refere_tokens, nuance_gen_tokens, numb_ents)
recall_nuance_genfast   = pseudo_recall(refere_tokens, nuance_genfast_tokens, numb_ents)
recall_nuance_genfast_p = pseudo_recall(refere_tokens, nuance_genfast_p_tokens, numb_ents)
recall_amazon = pseudo_recall(refere_tokens, amazon_tokens, numb_ents)

df2 = df[["contact_id", "file_id", "reference", "nuance_gen", "nuance_genfast", "nuance_genfast_p", "amazon"]]

df2["recall_nuance_gen"] = recall_nuance_gen[4]
df2["recall_nuance_genfast"] = recall_nuance_genfast[4]
df2["recall_nuance_genfast_p"] = recall_nuance_genfast_p[4]
df2["recall_amazon"] = recall_amazon[4]

# precision
precis_nuance_gen = pseudo_precision(refere_tokens, nuance_gen_tokens, numb_ents)
precis_nuance_genfast = pseudo_precision(refere_tokens, nuance_genfast_tokens, numb_ents)
precis_nuance_genfast_p = pseudo_precision(refere_tokens, nuance_genfast_p_tokens, numb_ents)
precis_amazon = pseudo_precision(refere_tokens, amazon_tokens, numb_ents)

df2["precision_nuance_gen"] = precis_nuance_gen[4]
df2["precision_nuance_genfast"] = precis_nuance_genfast[4]
df2["precision_nuance_genfast_p"] = precis_nuance_genfast_p[4]
df2["precision_amazon"] = precis_amazon[4]

df2 = df2[
    [
        "contact_id",
        "file_id",
        "reference",
        "nuance_gen",
        "recall_nuance_gen",
        "precision_nuance_gen", 
        "nuance_genfast", 
        "recall_nuance_genfast",
        "precision_nuance_genfast",
        "nuance_genfast_p", 
        "recall_nuance_genfast_p",
        "precision_nuance_genfast_p",
        "amazon",
        "recall_amazon",
        "precision_amazon"
    ]
]

df2.to_excel("../../results/nums_ents_nuance_vs_amazon.xlsx", index=False)

# f1-score
f1_score_nuance_gen = f1_score(precis_nuance_gen[5], recall_nuance_gen[5])
f1_score_nuance_genfast = f1_score(precis_nuance_genfast[5], recall_nuance_genfast[5])
f1_score_nuance_genfast_p = f1_score(precis_nuance_genfast_p[5], recall_nuance_genfast_p[5])
f1_score_amazon = f1_score(precis_amazon[5], recall_amazon[5])

# ---# banking entities #---#
bank_ents = read_entity("../data/bank_entities.txt")

# recall
recall_nuance_gen = pseudo_recall(refere_tokens, nuance_gen_tokens, bank_ents)
recall_nuance_genfast = pseudo_recall(refere_tokens, nuance_genfast_tokens, bank_ents)
recall_nuance_genfast_p = pseudo_recall(refere_tokens, nuance_genfast_p_tokens, bank_ents)
recall_amazon = pseudo_recall(refere_tokens, amazon_tokens, bank_ents)

df3 = df[["contact_id", "file_id", "reference", "nuance_gen", "nuance_genfast", "nuance_genfast_p", "amazon"]]

df3["recall_nuance_gen"] = recall_nuance_gen[4]
df3["recall_nuance_genfast"] = recall_nuance_genfast[4]
df3["recall_nuance_genfast_p"] = recall_nuance_genfast_p[4]
df3["recall_amazon"] = recall_amazon[4]

# precision
precis_nuance_gen = pseudo_precision(refere_tokens, nuance_gen_tokens, bank_ents)
precis_nuance_genfast = pseudo_precision(refere_tokens, nuance_genfast_tokens, bank_ents)
precis_nuance_genfast_p = pseudo_precision(refere_tokens, nuance_genfast_p_tokens, bank_ents)
precis_amazon = pseudo_precision(refere_tokens, amazon_tokens, bank_ents)

df3["precision_nuance_gen"] = precis_nuance_gen[4]
df3["precision_nuance_genfast"] = precis_nuance_genfast[4]
df3["precision_nuance_genfast_p"] = precis_nuance_genfast_p[4]
df3["precision_amazon"] = precis_amazon[4]

df3 = df3[
    [
        "contact_id",
        "file_id",
        "reference",
        "nuance_gen",
        "recall_nuance_gen",
        "precision_nuance_gen", 
        "nuance_genfast", 
        "recall_nuance_genfast",
        "precision_nuance_genfast",
        "nuance_genfast_p", 
        "recall_nuance_genfast_p",
        "precision_nuance_genfast_p",
        "amazon",
        "recall_amazon",
        "precision_amazon"
    ]
]

df3.to_excel("../../results/bank_ents_nuance_vs_amazon.xlsx", index=False)

# f1-score
f1_score_nuance_gen = f1_score(precis_nuance_gen[5], recall_nuance_gen[5])
f1_score_nuance_genfast = f1_score(precis_nuance_genfast[5], recall_nuance_genfast[5])
f1_score_nuance_genfast_p = f1_score(precis_nuance_genfast_p[5], recall_nuance_genfast_p[5])

f1_score_amazon = f1_score(precis_amazon[5], recall_amazon[5])
