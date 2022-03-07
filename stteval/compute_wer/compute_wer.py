import numpy as np


def compute_levenshtein_distance(s1: list, s2: list) -> int:
    """Compute levenshtein distance using tokens as the reference unity."""
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, w1 in enumerate(s1):
        current_row = [i + 1]
        for j, w2 in enumerate(s2):
            insertions = (
                previous_row[j + 1] + 1
            )  # j+1 instead of j since previous_row and current_row are one word longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (w1 != w2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def count_wildcards_in_reference(references: list) -> int:
    """Count the number of tokens inside the square brackets [] for each transcription in the 'references' list."""
    in_square_brackets = (
        False  # indicates whether or not a given token is inside the "[]""
    )
    wildcard_counts = []  # list to stock the sum of the words inside the "[]""
    for reference in references:
        wildcard = 0
        for token in reference:
            if in_square_brackets:
                if token == "]":
                    in_square_brackets = False  # stop counting
                else:
                    wildcard += 1
            else:
                if token == "[":
                    in_square_brackets = True  # start counting
        wildcard_counts.append(wildcard)
    return wildcard_counts


def compute_wer(references: list, transcripts: list) -> (list, float):
    """Compute the WER for each transcription and compute the global wer for evaluate the whole engin"""
    wildcards = count_wildcards_in_reference(
        references
    )  # number of wildcards to be substracted on each transcription
    references_clean = [
        [word for word in sentence if word not in ["[", "]"]] for sentence in references
    ]  # eliminate the [], so they are not counted in the computation
    words_in_reference = [len(sentence) for sentence in references_clean]
    distances = [
        compute_levenshtein_distance(reference, transcript)
        for reference, transcript in zip(references_clean, transcripts)
    ]
    wer = (np.array(distances) - np.array(wildcards)) / np.array(words_in_reference)
    global_wer = sum(wer) / len(references)
    print("WER : ", global_wer)
    return wer, global_wer
