sentence ="a b asdf fdsa"
totalWords = len([word for word in sentence.split() if word.isalpha()])
print(totalWords)