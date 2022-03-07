import numpy as np
from collections import Counter


def pseudo_recall(references, transcripts, entities):
    """Compute the % of entities in the reference that have been correctly transcribe by the engin.

    Parameters
    ----------
    references :
        list of tokens from the reference.
    transcripts :
        list of tokens from the transcription generated by the engin we want to evaluate.
    entities :
        list of entities we want to evaluate on.

    Returns
    -------
    number_errors_list
        number of errors in each sentence.
    entity_errors_list
        entities producing errors in each sentence.
    number_ref_list
        number of entities each reference sentence.
    entity_ref_list
        entities in each reference sentence.
    pseudo_recall
        recall for each sentence.
    global_pseudo_recall
        global corpus' recall.

    """
    number_errors_list = []  # number of errors for each sentence
    entity_errors_list = (
        []
    )  # specific entities used to count the errors for each sentence (i.e. len(entity_errors_list) = number_errors_list )
    number_ref_list = []  # number of entities in the reference for each sentence
    entity_ref_list = (
        []
    )  # specific entities contained in the reference for each sentence

    for reference, transcript in zip(references, transcripts):
        transcript_counter = Counter(transcript)
        ref_counter = Counter(reference)
        number_errors = 0  # number of errors in each sentence
        entity_errors = []  # entities used to count the errors
        number_ref = 0  # number of entities in each sentence
        entity_ref = []  # entities identified in the reference
        for entity in entities:
            if ref_counter[entity]:  # the entity is in the reference
                number_ref += ref_counter[entity]  # count all entities
                entity_ref.append(entity)
                if transcript_counter[entity]:  # the entity is in the transcription
                    number_errors += max(
                        0, ref_counter[entity] - transcript_counter[entity]
                    )
                    if (
                        ref_counter[entity] > transcript_counter[entity]
                    ):  # but is missing in the transcription
                        entity_errors.append(entity)
                else:  # the entity has been omited by the engin
                    number_errors += ref_counter[entity]
                    entity_errors.append(entity)

        number_errors_list.append(number_errors)  # number of errors for each sentence
        entity_errors_list.append(
            entity_errors
        )  # specific entities contained in the reference for each sentence

        number_ref_list.append(
            number_ref
        )  # number of entities in the reference for each sentence
        entity_ref_list.append(
            entity_ref
        )  # specific entities used to count the errors for each sentence (i.e. len(entity_errors_list) = number_errors_list )

        pseudo_recall = 1 - (np.array(number_errors_list) / np.array(number_ref_list))

    print("Total number of errors : ", sum(number_errors_list))
    print("Total number of entities : ", sum(number_ref_list))
    global_pseudo_recall = 1 - (sum(number_errors_list) / sum(number_ref_list))
    print("Recall : ", global_pseudo_recall)

    return (
        number_errors_list,
        entity_errors_list,
        number_ref_list,
        entity_ref_list,
        pseudo_recall,
        global_pseudo_recall,
    )


def pseudo_precision(references, transcripts, entities):
    """Compute the % of entities in the transcription that are included in the reference.

    Parameters
    ----------
    references :
        list of tokens from the reference.
    transcripts :
        list of tokens from the transcription generated by the engin we want to evaluate.
    entities :
        list of entities we want to evaluate on.

    Returns
    -------
    number_errors_list
        number of errors in each sentence.
    entity_errors_list
        entities producing errors in each sentence.
    number_trans_list
        number of entities each transcription sentence.
    entity_trans_list
        entities in each transcription sentence.
    pseudo_precision
        precision for each sentence.
    global_pseudo_precision
        global corpus' precision.

    """
    number_errors_list = []  # number of errors for each sentence
    entity_errors_list = (
        []
    )  # specific entities used to count the errors for each sentence (i.e. len(entity_errors_list) = number_errors_list )
    number_trans_list = []  # number of entities in the transcription for each sentence
    entity_trans_list = (
        []
    )  # specific entities contained in the transcription for each sentence

    for reference, transcript in zip(references, transcripts):
        transcript_counter = Counter(transcript)
        ref_counter = Counter(reference)
        number_errors = 0  # number of errors in each sentence
        entity_errors = []  # entities used to count the errors
        number_trans = 0  # number of entities in each sentence
        entity_trans = []  # entities identified in the transcription
        for entity in entities:
            if transcript_counter[entity]:  # if the entity appears in the transcription
                number_trans += transcript_counter[entity]  # count all entities
                entity_trans.append(entity)
                if (
                    transcript_counter[entity] > ref_counter[entity]
                ):  # if the entity appears in the transcription, but not in the reference
                    number_errors += (
                        transcript_counter[entity] - ref_counter[entity]
                    )  # count the adds as errors
                    entity_errors.append(entity)

        number_errors_list.append(number_errors)
        entity_errors_list.append(entity_errors)
        number_trans_list.append(number_trans)
        entity_trans_list.append(entity_trans)

        pseudo_precision = 1 - (
            np.array(number_errors_list) / np.array(number_trans_list)
        )

    print("Total number of errors : ", sum(number_errors_list))
    print("Total number of entities : ", sum(number_trans_list))
    global_pseudo_precision = 1 - (sum(number_errors_list) / sum(number_trans_list))
    print("Precision", global_pseudo_precision)

    return (
        number_errors_list,
        entity_errors_list,
        number_trans_list,
        entity_trans_list,
        pseudo_precision,
        global_pseudo_precision
    )


def f1_score(precision_global, recall_global):
    """Compute f1-score

    Parameters
    ----------
    precision_global :
        (float) global precision outputed by the pseudo_precision function.
    recall_global :
        (float)  global recall outputed by the pseudo_recall function

    Returns
    -------
    f1_score_global
        (float) f1-score overall corpus
    f1_score_list
        (list) f1-score for each sentence in the corpus

    """
    f1_score_global = 2 * (
        (precision_global * recall_global) / (precision_global + recall_global)
    )
    print(f1_score_global)
    return f1_score_global