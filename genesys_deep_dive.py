import pandas as pd

my_wd = "C:/Users/mard019/Desktop/Documents/Git/STTevaluator/"

reference = read_reference(
    cols=["Transcription corrigée", "Contact ID"],
    path=my_wd + "data/references.csv",
)
reference.head()

genesys_topics = read_genesys_trans(path=my_wd + "data/genesys_topics.csv")
genesys_topics.head()