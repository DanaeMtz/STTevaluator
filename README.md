# STT evaluator



# Motivation

This set of functions have been created in order to evaluate and compare speech-to-text engines attached to different conversational AI solutions. The metrics to be considered are described below. 

## Word Error Rate (WER)

Is a common metric for measuring speech-to-text accuracy of automatic speech recognition (ASR) systems. It is computed as the number of errors divided by the total number of words.

Word Error Rate = (Substitutions + Insertions + Deletions) / Number of Words Spoken in the reference transcript 

Where errors are:

- Substitution: when a word is replaced (for example, “shipping” is transcribed as “sipping”)
- Insertion: when a word that wasn't said is added (for example, “hostess” is transcribed as “host is”)
- Deletion: when a word is omitted from the transcript (for example, “get it done” is transcribed as “get done”)

## Entity evaluation

We seek to evaluate the ability of STT engines to correctly identify a certain set of entities. When making this evaluation, there are two different types of errors that can occur:

- The entity is in the reference, but it was missed by the system (mistranscribed or omitted).
- The entity appears incorrectly in the transcription.

In order to evaluate these two types of errors, we will consider the following performance measures:

- **Recall**: % of entities in the reference that were correctly transcribed.           
1- (number of entities in the transcript that were incorrectly transcribed or omitted/total number of entities in the reference)

- **Precision**: % of entities in the transcript that are in the reference.
1 - (number of erroneously added entities in the transcript / total number of entities in the transcript)

- **F1-score**: harmonic mean that combines precision and recall. Gives a measure of overall performance.
2( Precision x Recall / Precision + Recall )

The entities considered in this exercise are:

- Words that represent numbers: \{ zéro, un, deux, trois, quatre, cinq, six, sept, huit, neuf, dix, onze, douze, treize, quatorze, quinze, seize, dix, vingt, trente, quarante, cinquante, soixante, cent, mille. \}
- Words specific to the banking industry: \{ celi, cri, reer, cpg, ferr, natgo, nip, reee, bni, rap, bnc. \}



### Results 

| Engin   | WER | WER (with lemmatization) |
|---------|-----|-----|
| Nuance  |0.09 |0.08 |
| Verint  |0.39 |0.37 |
| Genesys |0.15 |0.13 |

**banking entities**

| Engin   | Recall | Precision | F1-score |
|---------|--------|-----------|----------|
| Nuance  |0.92    |1.00       |0.96      |
| Verint  |0.22    |0.55       |0.32      |
| Genesys |0.04    |1.00       |0.08      |

**numeric entities (corpus of numbers 61)**

| Engin   | Recall | Precision | F1-score |
|---------|--------|-----------|----------|
| Nuance  | 0.93   |  0.93     | 0.93     |
| Genesys | 0.97   |  0.98     | 0.98     |

**numeric entities**

| Engin   | Recall | Precision | F1-score |
|---------|--------|-----------|----------|
| Nuance  | 0.92   | 0.90      | 0.91     |
| Verint  | 0.61   | 0.77      | 0.68     |
| Genesys | 0.90   | 0.91      | 0.91     |

#### Examples of common mistakes 

| Engin      | Transcript |
|------------|------------|
| Reference  |présentement j'ai subi un vol d'identité.|
| Nuance     |présentement j'ai subi un vol d'identité |
| Genesys    |présentement j'ai **su bien** vol d'identités|
| Verint     |présentement je **suis bien** vol d'identité |

| Engin      | Transcript |
|------------|------------|
| Reference  |Allô oui bonjour, ce serait pour mon CELI, dans le fond je voudrais faire de l'épargne systématique|
| Nuance     |Allô oui bonjour ça serait pour mon CELI dans le fond je voudrais faire de l'épargne systématique|
| Genesys    |allô oui bonjour euh ce serait **prononcé lui** dans le chan je voudrais faire de **lepage** systématique|
| Verint     |     oui bonjour ce serait **pour mon pays** dans le fond je voudrais faire **les taxes** était matché qu'|

| Engin      | Transcript |
|------------|------------|
| Reference  |j'avais fait un virement en date du 28 mai à ma fille qui qui elle fait partie de la Caisse Populaire Desjardins|
| Nuance     |j'avais fait un virement en date du 28 mai à ma fille qui qui elle fait partie de la Caisse Populaire Desjardins|
| Genesys    |j'avais fait un virement en date du **28 mille** ma fille qui qui fait partie de la casse plus la de jardin|
| Verint     |j' avais un virement en date du **28 - marie** puis elle fait partie après|

| Engin      | Transcript |
|------------|------------|
| Reference  |J'appelle pour avoir de l'information sur un taux hypothécaire pour acheter une maison.|
| Nuance     |J'appelle pour avoir de l'information sur un taux hypothécaire pour acheter une maison|
| Genesys    |j'appelle **revoir** de l'information sur un **tour hypothèse** pour acheter une maison|
| Verint     |j'appelle qu' on va l' information sur un peu quoi c' est ça qui maison |


| Engin      | Transcript |
|------------|------------|
| Reference  |je voudrais faire trois arrêts de paiement.|
| Nuance     |je voudrais faire trois arrêts de paiement |
| Genesys    |je voudrais faire trois arrête **ment**|
| Verint     |moi je regarde c' est même |


| Engin      | Transcript |
|------------|------------|
| Reference  |c'est parce qu'on s'est fait **piraté** notre courriel notre **cellulaire**|
| Nuance     |    c'parce qu'on s'est fait pirater notre courriel notre cellulaire|
| Genesys    |      parce qu'on se fait **puis rater** notre courriel **à celle là**|
| Verint     |c'était - sept neuf quatre comment c'est quatre qui est gratuit notre **et elle**|


It is difficult fot the genesys and the verint engines to recognize specific domain banking words, such as CELI and REER. Let's see some examples. 


| Engin      | Transcript |
|------------|------------|
| Reference  |j'aimerais avoir le solde de mon CELI|
| Nuance     |j'aimerais avoir le solde de mon CELI|
| Genesys    |j'aimerais avoir le **sol** de mon **sali**|
|            |j'aimerais avoir le **sol** de mon **série**|
| Verint     |j'aimerais avoir le solde de mon **c'est dit**|


| Engin      | Transcript |
|------------|------------|
| Reference  |je voudrais échanger mes points pour de l'argent de le mettre dans mon CELI|
| Nuance     |je voudrais **changer** mes points pour de l'argent de le mettre dans mon CELI|
| Genesys    |je voudrais **changer** mes points pour de l'argent de le mettre dans mon **élise**|
| Verint     |je voudrais échanger mes points pour euh l'argent de le mettre dans mon **cellulaire**|


| Engin      | Transcript |
|------------|------------|
| Reference  |je voudrais retirer 300 pièces de mon CELI|
| Nuance     |je voudrais retirer trois cent pièces de mon CELI|
| Genesys    |je voudrais retirer trois cent pièces de mon **série**|
| Verint     |je voudrais euh **soixante** piastres de mon **ancien lui**|

| Engin      | Transcript |
|------------|------------|
| Reference  |j'aimerais ça faire une cotisation pour mon REER.|
| Nuance     |j'aimerais ça faire une cotisation pour mon REER|
| Genesys    |j'aimerais ça faire une cotisation pour montréal|
| Verint     | vide |

| Engin      | Transcript |
|------------|------------|
| Reference  |j'ai fait une ouverture de compte épargne comme je suis nouveau à BNC|
| Nuance     |j'ai fait une ouverture de compte épargne comme je suis nouveau à BNC|
| Genesys    |j'ai fait une ouverture de compte **pan** comme **ce ce** nouveau **euh a bien ce**|
| Verint     |j' ai -  |

Genesys seems to be very sensitive to the accents. We have observed some lack of consistent in the transcripts, since the same call is usually transcribed differently when we have different speakers. 

**Numbers**

The examples below come from the numbers corpus containing 61 recordings

| Engin      | Transcript |
|------------|------------|
| Reference  |J'aimerais céduler **un** paiement mensuel de **vingt sept** dollar et **cinquante cinq** sous qui sera versé tous les **15** du mois à partir d'octobre.|
| Nuance     |J'aimerais *c'est Jul* un paiement mensuel de 27,55 $ qui sera versé tous les 15 du mois à partir d'octobre|
| Genesys    |j'aimerais cédule *mon mensuel* de **vingt sept** dollars et **cinquante cinq** sous qui se traversée tous les **quinze** du mois à partir d'octobre|


| Engin      | Transcript |
|------------|------------|
| Reference  |Transfert **mille** dollars et **cent dix** et un autre **deux mille soixante douze** dollars et **douze** sous de mon compte CELI le **20** novembre|
| Nuance     |Transfert 1000 \$ et 70 autres 2072,12 $ de mon compte CELI le 20 novembre|
| Genesys    |Transfert **mille** dollars et **cent dix** et un autre **deux mille soixante douze** dollars et **douze** sous de mon compte série le **vingt** novembre|


| Engin      | Transcript |
|------------|------------|
| Reference  |J'aimerais céduler un paiement mensuel de **quarante neuf** dollar et **quatrante neuf** sous tous le 11 du mois à partir d'avril 2022.|
| Nuance     |Ma cellulaire un paiement mensuel de 49,49 $ tout les 11 du mois à partir d'avril 2022|
| Genesys    |je m'a schédulé un demi mensuel de **quarante neuf** dollars et **quand le** sous tous les onze du mois à partir d'avril deux mille vingt deux|

Remark that Nuance make the parsing if the number is followed by a word indicating amount, such as dollars or sous. The examples followed below represent the come from the original corpus. 

| Engin      | Transcript |
|------------|------------|
| Reference  |appelez le 1 888 835 6281 pour vérifier votre carte avec Apple Pay.|
| Nuance     |appeler le 1-888-835-6281 pour vérifier votre carte avec ApplePay|
| Genesys    |appeler le un huit huit huit euh huit trois cinq six deux huit un pour vérifier votre carte avec app|
| Verint     |appeler le un huit huit huit euh huit trois cinq six deux huit un pour vérifier votre carte avec - p|

| Engin      | Transcript |
|------------|------------|
| Reference  |m'ont donné un numéro de téléphone 414 413 5527, et puis c'est pas bon ce numéro là.|
| Nuance     |m'ont donné un numéro de téléphone 414-413-5527 et puis c'est pas bon ce numéro là|
| Genesys    |ont donné un numéro de téléphone euh quatre un quatre quatre un trois cinq cinq deux sept et puis c'est pas bon ce|
| Verint     |plan en donner un numéro de téléphone euh pas puis un quatre quatre un trois cinq cinq deux sept - pour voir ce numéro là|

In conclusion, Genesys is as good as nuance with numbers, except that nuance has parsing integrated. 


# Tech/Framework used
This is used to help the reader understand which tech or frameworks have been used to do the project. It helps the reader understand which all tech stack he has to be familiar with to understand the whole project.

# Features
This is where you write what all extra features have been done in your project. Basically this is where you try to make your project stand out from the rest.

# Code Examples
This is where you try to compress your project and make the reader understand what it does as simply as possible. This should help the reader understand if your code solves their issue.

# How to Use?
As I have mentioned before, you never know who is going to read your readme. So it is better to provide information on how to use your project. A step-by-step guide is best suited for this purpose. It is better to explain steps as detailed as possible because it might be a beginner who is reading it.
