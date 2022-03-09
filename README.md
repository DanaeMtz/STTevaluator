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

### Results 

| Engin   | WER |
|---------|-----|
| Nuance  |0.09 |
| Verint  |0.39 |
| Genesys |0.15 |

#### Examples of common mistakes 


| Engin      | Transcript |
|------------|------------|
| Reference  |présentement j'ai subi un vol d'identité.|
| Nuance     |présentement j'ai subi un vol d'identité |
| Verint     |présentement je **suis bien** vol d'identité |
| Genesys    |présentement j'ai **su bien** vol d'identités|

| Engin      | Transcript |
|------------|------------|
| Reference  |je voudrais faire trois arrêts de paiement.|
| Nuance     |je voudrais faire trois arrêts de paiement |
| Verint     |moi je regarde c' est même |
| Genesys    |je voudrais faire trois arrête **ment**|


| Engin      | Transcript |
|------------|------------|
| Reference  |Allô oui bonjour, ce serait pour mon CELI, dans le fond je voudrais faire de l'épargne systématique|
| Nuance     |Allô oui bonjour ça serait pour mon CELI dans le fond je voudrais faire de l'épargne systématique|
| Verint     |     oui bonjour ce serait **pour mon pays** dans le fond je voudrais faire **les taxes** était matché qu'|
| Genesys    |allô oui bonjour euh ce serait **prononcé lui** dans le chan je voudrais faire de **lepage** systématique|


| Engin      | Transcript |
|------------|------------|
| Reference  |J'appelle pour avoir de l'information sur un taux hypothécaire pour acheter une maison.|
| Nuance     |J'appelle pour avoir de l'information sur un taux hypothécaire pour acheter une maison|
| Verint     |j'appelle qu' on va l' information sur un peu quoi c' est ça qui maison |
| Genesys    |j'appelle **revoir** de l'information sur un **tour hypothèse** pour acheter une maison|


| Engin      | Transcript |
|------------|------------|
| Reference  |c'est parce qu'on s'est fait **piraté** notre courriel notre **cellulaire**|
| Nuance     |    c'parce qu'on s'est fait pirater notre courriel notre cellulaire|
| Verint     |c'était - sept neuf quatre comment c'est quatre qui est gratuit notre **et elle**|
| Genesys    |      parce qu'on se fait **puis rater** notre courriel **à celle là**|


# Build Status

This basically explains the current build status of the project. If there is a bug /error which needs addressing. This is done so for two different reasons The user understands that this is an issue and does not spend more time figuring if it was a mistake on their part.A developer who is familiar with the issue can suggest some solutions directly without going through the whole code.

# Code Style
This lets the users know that you have used a particular code style and helps them when contributing to your project so that the whole project code style stays the same. Some common code styles: standard, xo, etc.

# Screenshots
As the saying goes, a picture is equal to a thousand words. Most people will be interested if there is a visual representation of what the project is about. It helps them understand better. A visual representation can be snapshots of the project or a video of the functioning of the project.

# Tech/Framework used
This is used to help the reader understand which tech or frameworks have been used to do the project. It helps the reader understand which all tech stack he has to be familiar with to understand the whole project.

# Features
This is where you write what all extra features have been done in your project. Basically this is where you try to make your project stand out from the rest.

# Code Examples
This is where you try to compress your project and make the reader understand what it does as simply as possible. This should help the reader understand if your code solves their issue.

# Installation
If your project needs installation of certain software or configurations to the system. Do mention it in this section as it helps a lot for the reader to use your project. The steps mentioned should be precise and explanatory.  If possible, you can add links that can help them better understand how to configure/install the necessary files or softwares.

# API reference
If your project is small, then we can add the reference docs in the readme. For larger projects, it is better to provide links to where the API reference documentation is documented.
Tests
This is the section where you mention all the different tests that can be performed with code examples

# How to Use?
As I have mentioned before, you never know who is going to read your readme. So it is better to provide information on how to use your project. A step-by-step guide is best suited for this purpose. It is better to explain steps as detailed as possible because it might be a beginner who is reading it.

# Contribute
This is where you let them know that they can contribute and help you out. A guideline on how to contribute is also helpful

# Credits
Giving proper credit is most important. Mention any links/repos which helped you or inspired you to build this project. It can be a blog, another open source project, or just people who have contributed in building this project.

# License
A short description of the license. (MIT, Apache, etc.)