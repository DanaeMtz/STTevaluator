import pandas as pd
import os
import json
import re
from stteval.utils import flat_list


def read_reference(cols: list, path: str):
    """Read cvs file containing the reference text."""
    df = pd.read_csv(
        path, usecols=cols, encoding="latin-1", dtype={"Contact ID": "str"}
    )
    df.dropna(inplace=True)
    df = df.rename(
        columns={"Transcription corrigée": "reference", "Contact ID": "contact_id"}
    )
    return df


def read_entity(path: str) -> list:
    """Read .txt file containing the entities used to evaluation."""
    with open(path, encoding="utf-8") as f:
        entities = [line.rstrip() for line in f]
    return entities


def read_json_file(path: str):
    """Read the corresponding json file and extract the transcription."""
    with open(path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    return json_data["results"]["transcripts"][0]["transcript"]


def read_amazon_trans(path: str):
    """Generate a pandas dataframe containing the Contact id and the
    corresponding transcription produced by Amazon Lex."""
    json_files = [
        pos_json for pos_json in os.listdir(path) if pos_json.endswith(".json")
    ]  # create a list with the file's names
    json_files_t = list(
        filter(re.compile(r"\d{6,19}_\w+").search, json_files)
    )  # read only the files containing the transcriptions

    json_data = []
    for file in json_files_t:
        json_data.append(
            [
                file.split("_")[0],
                re.findall(r"\d{6,19}_\w+", file)[0],
                read_json_file(path + "/" + str(file)),
            ]
        )  # separeate contact ID (all digits before the "_") from the file's name and store them separately
    df = pd.DataFrame(json_data, columns=["contact_id", "file_id", "amazon"])
    return df


def read_nuance_trans(path: str, enc="utf-8"):
    """read transcription produced by Nuance Mix."""
    df = pd.read_csv(path, encoding=enc)
    file_id = flat_list([re.findall(r"(\d{6,19}_\w+)", ids) for ids in df.iloc[:, 0]])
    contact_id = flat_list([re.findall(r"(\d{6,19})", ids) for ids in df.iloc[:, 0]])
    df["file_id"] = file_id
    df["contact_id"] = contact_id
    df = df.drop(["FileName"], axis=1)
    df = df.rename(columns={"TranscriptionNuance": "nuance"})
    return df


def read_genesys_trans(path: str, enc="utf-8"):
    """read transcription produced by genesys."""
    df = pd.read_csv(path, encoding=enc)
    file_id = flat_list([re.findall(r"(\d{6,19}_\w+)", ids) for ids in df.iloc[:, 0]])
    contact_id = flat_list([re.findall(r"(\d{6,19})", ids) for ids in df.iloc[:, 0]])
    df["file_id"] = file_id
    df["contact_id"] = contact_id
    df = df.drop(["name"], axis=1)
    df = df.rename(columns={"transcript": "genesys"})
    return df
