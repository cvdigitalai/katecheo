from fuzzywuzzy import fuzz

def getMatch(original, compare):
  return fuzz.ratio(original, compare)

