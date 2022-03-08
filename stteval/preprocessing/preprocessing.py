import spacy
import re
import num2words


def reference_preprocessing(sentences: list) -> list:
    """Perform preprocessing for the particularities of reference text:
    1. Covert all words into lower case
    2. Remove "." and ","
    3. Turn the numbers into words
    4. Turn the euh into [hésitation]
    5. Remove double spaces
    """
    reference_mod1 = [
        re.sub(
            r"(?P<integer>\d+),(?P<decimal>\d+)", "\g<integer>.\g<decimal>", sentence
        )
        for sentence in sentences
    ]
    reference_mod2 = [
        re.sub(
            # r"[,]?[.]?[\d]+[.,]?[\d]?",
            r"\d+",
            lambda m: num2words.num2words(m.group(0), lang="fr").replace("-", " "),
            sentence,
        )
        for sentence in reference_mod1
    ]
    reference_mod3 = [
        re.sub(
            r"(?P<last_int>\w+)\.(?P<first_dec>\w+)",
            "\g<last_int> et \g<first_dec>",
            sentence,
        )
        for sentence in reference_mod2
    ]
    reference_mod4 = [re.sub(r"\beuh\b", "[hésitation]", ref) for ref in reference_mod3]
    reference_mod5 = [re.sub(r"-", " ", sentence) for sentence in reference_mod4]
    reference_mod6 = [re.sub(r"\s+", " ", sentence) for sentence in reference_mod5]
    reference_mod7 = [
        re.sub(r"[.,]", "", sentence.lower()) for sentence in reference_mod6
    ]
    return reference_mod7


def verint_preprocessing(sentences: list) -> list:
    """Perform text preprocessing for the particularities of the Verint transcription :
    Covert word into lower case
    Remove the white spaces after the " ' " sign (example: j' ai);
    Remove the symbol " - " followed by a white space;
    Remove "." and ",".
    """
    verint_mod1 = [re.sub(r"' ", "'", sentence.lower()) for sentence in sentences]
    verint_mod2 = [re.sub(r"\.|,|-\s|", "", sentence) for sentence in verint_mod1]
    verint_mod3 = [re.sub(r"\s+", " ", sentence) for sentence in verint_mod2]
    return verint_mod3


def amazon_preprocessing(sentences: list) -> list:
    """Perform text preprocessing for the particularities of the Amazon Lex transcription :
    Covert word into lower case;
    Remove "." and ",";
    Remove the symbol "-" appearing in numbers.
    """
    amazon_mod1 = [re.sub(r"\.|,", "", sentence.lower()) for sentence in sentences]
    amazon_mod2 = [re.sub(r"-", " ", sentence) for sentence in amazon_mod1]
    return amazon_mod2


def nuance_preprocessing(sentences: list) -> list:
    """Perform text preprocessing for the particularities of the Nuance Mix transcription :
    1. Remove "." and ",".
    2. Covert words into lower case.
    3. Turn numbers to words (and the $ sign to the word dollars).
    4. Eliminate double spaces.
    4. Remove the symbol "-" appearing in numbers.
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


def genesys_preprocessing(sentences: list) -> list:
    """eliminate words representing hesitations"""
    reference_mod1 = [re.sub(r"\beuh\b", "", ref) for ref in sentences]
    reference_mod2 = [re.sub(r"\s+", " ", sentence) for sentence in reference_mod1]
    return reference_mod2


def tokenize_lemmatize(sentenses: list) -> list:
    """Generate lemmatized tokens using spacy"""
    nlp = spacy.load("fr_core_news_md")
    tokenizer = nlp.tokenizer
    tokenized_lemmatized_sentences = [
        [token.lemma_ for token in tokenizer(sentence)] for sentence in sentenses
    ]
    lemmatized_sentences = [
        " ".join(tokens) for tokens in tokenized_lemmatized_sentences
    ]
    return tokenized_lemmatized_sentences, lemmatized_sentences


def tokenize(sentenses: list) -> list:
    """Generate tokens using spacy"""
    nlp = spacy.load("fr_core_news_md")
    tokenizer = nlp.tokenizer
    tokenized_sentences = [
        [token.text for token in tokenizer(sentence)] for sentence in sentenses
    ]
    return tokenized_sentences


def clean_genesys_tokens(tokens: list) -> list:
    """Eliminate numbers at the begining of the transcription"""
    it_nums = []
    for number in range(25):
        it_nums.append(num2words.num2words(number + 1, lang="fr"))
        it_nums = [re.sub(r"-", " ", sentence) for sentence in it_nums]

    numbs_tokens = tokenize(it_nums)
    flat_numbs = [item for sublist in numbs_tokens for item in sublist]
    flat_numbs = list(dict.fromkeys(flat_numbs))
    flat_numbs_ = [x for x in flat_numbs if x != "et"]

    new_tokens = []
    for trans in tokens:
        if (
            (trans[0] in flat_numbs)
            and (trans[1] in flat_numbs)
            and (trans[2] in flat_numbs_)
        ):
            trans = trans[3:]
        elif (trans[0] in flat_numbs) and (trans[1] in flat_numbs):
            trans = trans[2:]
        elif trans[0] in flat_numbs or trans[0] == " ":
            trans = trans[1:]
        else:
            trans = trans
        new_tokens.append(trans)
    return new_tokens
