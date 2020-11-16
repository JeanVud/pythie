basePath = "/home/giangvdq/data"
docwordPath = basePath + """/docword.{}.txt.gz"""
vocabPath   = basePath + """/vocab.{}.txt."""

PATHS = {
    "docword" : {
        'enron':    docwordPath.format("enron"),
        'kos':      docwordPath.format("kos"),
        'nips':     docwordPath.format("nips"),
        'nytimes':  docwordPath.format("nytimes"),
        'pubmed':   docwordPath.format("pubmed"),

    },
    "vocab" : {
        'enron':    vocabPath.format("enron"),
        'kos':      vocabPath.format("kos"),
        'nips':     vocabPath.format("nips"),
        'nytimes':  vocabPath.format("nytimes"),
        'pubmed':   vocabPath.format("pubmed"),

    }
}