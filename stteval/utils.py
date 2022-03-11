from collections import Counter


def flat_list(my_list_of_lists):
    """Turn a list of lists into a flat list

    Args:
      my_list_of_lists: 

    Returns:

    Raises:

    """
    flat_list = []
    for sublist in my_list_of_lists:
        for item in sublist:
            flat_list.append(item)
    return flat_list 


def get_entities(entities, counter_tokens):
    """
    Get the counts corresponding to the tokens included in the entities list
    Args:
    entities (list) : a list of entities we want to filter 
    counter_tokens (dict) : a dictionary containing the counts of tokens in a given sentence. 
    """
    counter_ent_tokens = {}
    for entity in entities: 
        if counter_tokens[entity] > 0:
            counter_ent_tokens[entity] = counter_tokens[entity]
    return counter_ent_tokens
