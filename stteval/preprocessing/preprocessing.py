import spacy
import re
import num2words


def reference_preprocessing(sentences):
    """Perform preprocessing for the particularities of reference text:
    Covert word into lower case
    Remove "." and ",
    Turn the numbers into words

    Parameters
    ----------
    sentences :
        a list containing the reference sentences

    Returns
    -------

    """
    reference_mod1 = [re.sub(r"(?P<integer>\d+),(?P<decimal>\d+)", "\g<integer>.\g<decimal>", sentence) for sentence in sentences]
    reference_mod2 = [
        re.sub(
            #r"[,]?[.]?[\d]+[.,]?[\d]?",
            r"\d+",
            lambda m: num2words.num2words(m.group(0), lang="fr").replace("-", " "),
            sentence,
        )
        for sentence in reference_mod1
    ]
    reference_mod3 = [re.sub(r"(?P<last_int>\w+)\.(?P<first_dec>\w+)", "\g<last_int> et \g<first_dec>", sentence) for sentence in reference_mod2]
    reference_mod4 = [re.sub(r"\beuh\b", "[hésitation]", ref) for ref in reference_mod3]
    reference_mod5 = [re.sub(r"-", " ", sentence) for sentence in reference_mod4]
    reference_mod6 = [re.sub(r"\s+", " ", sentence) for sentence in reference_mod5]
    reference_mod7 = [re.sub(r"[.,]", "", sentence.lower()) for sentence in reference_mod6]
    return reference_mod7


def verint_preprocessing(sentences):
    """Perform text preprocessing for the particularities of the Verint transcription :
    Covert word into lower case
    Remove the white spaces after the " ' " sign (example: j' ai);
    Remove the symbol " - " followed by a white space;
    Remove "." and ",".

    Parameters
    ----------
    sentences :
        a list containing the sentences from the Verint transcription

    Returns
    -------

    """
    verint_mod1 = [re.sub(r"' ", "'", sentence.lower()) for sentence in sentences]
    verint_mod2 = [re.sub(r"\.|,|-\s|", "", sentence) for sentence in verint_mod1]
    verint_mod3 = [re.sub(r"\s+", " ", sentence) for sentence in verint_mod2]
    return verint_mod3


def amazon_preprocessing(sentences):
    """Perform text preprocessing for the particularities of the Amazon Lex transcription :
    Covert word into lower case;
    Remove "." and ",";
    Remove the symbol "-" appearing in numbers.

    Parameters
    ----------
    sentences :
        a list containing the sentences from the Amazon transcription

    Returns
    -------

    """
    amazon_mod1 = [re.sub(r"\.|,", "", sentence.lower()) for sentence in sentences]
    amazon_mod2 = [re.sub(r"-", " ", sentence) for sentence in amazon_mod1]
    return amazon_mod2


def nuance_preprocessing(sentences):
    """Perform text preprocessing for the particularities of the Amazon Lex transcription :
    Covert word into lower case;
    Remove "." and ",";
    Remove the symbol "-" appearing in numbers.

    Parameters
    ----------
    sentences :
        a list containing the sentences from the Amazon transcription

    Returns
    -------

    """
    nuance_mod1 = [re.sub(r"\.|,", "", str(sentence.lower())) for sentence in sentences]
    nuance_mod2 = [
        re.sub(
            r"[,]?[.]?[\d]+[.,]?[\d]?",
            lambda m: num2words.num2words(m.group(0), lang="fr").replace("-", " "),
            sentence,
        )
        for sentence in nuance_mod1
    ]
    nuance_mod3 = [re.sub(r"\s+", " ", sentence) for sentence in nuance_mod2]
    nuance_mod4 = [re.sub(r"-", " ", sentence) for sentence in nuance_mod3]
    nuance_mod4 = [re.sub(r"\$", "dollars", sentence) for sentence in nuance_mod4]
    return nuance_mod4


def tokenize_lemmatize(sentenses):
    """Generate lemmatized tokens using spacy

    Parameters
    ----------
    sentenses : list
        List containing the sentenses to be tokenized and lemmatized.

    Returns
    -------

    """
    nlp = spacy.load("fr_core_news_md")
    tokenizer = nlp.tokenizer
    tokenized_lemmatized_sentences = [
        [token.lemma_ for token in tokenizer(sentence)] for sentence in sentenses
    ]
    lemmatized_sentences = [
        " ".join(tokens) for tokens in tokenized_lemmatized_sentences
    ]  # return the lemmatized_sentences to validation purposes
    return tokenized_lemmatized_sentences, lemmatized_sentences


def tokenize(sentenses):
    """Generate tokens using spacy

    Parameters
    ----------
    sentenses : list
        List containing the sentenses to be tokenized and lemmatized

    Returns
    -------

    """
    nlp = spacy.load("fr_core_news_md")
    tokenizer = nlp.tokenizer
    tokenized_sentences = [
        [token.text for token in tokenizer(sentence)] for sentence in sentenses
    ]
    return tokenized_sentences

