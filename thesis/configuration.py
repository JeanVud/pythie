basePath = "/home/giangvdq/data"
docwordPath = basePath + """/docword.{}.txt.gz"""
vocabPath   = basePath + """/vocab.{}.txt"""
mergedPath  = basePath + """/merged.{}.parquet"""

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

    },
    "merged" : {
        'enron':    mergedPath.format("enron"),
        'kos':      mergedPath.format("kos"),
        'nips':     mergedPath.format("nips"),
        'nytimes':  mergedPath.format("nytimes"),
        'pubmed':   mergedPath.format("pubmed"),

    }
}