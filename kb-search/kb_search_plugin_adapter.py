import gq_search_plugin_fuzzywuzzy

"""
  The GQ Search Plugin Adapter expects
    Input:
      1. The original string
      2. The string to compare against
  
  The return value will be the confidence value. Zero if not matching
"""
def getMatch(original, compare):
  return gq_search_plugin_fuzzywuzzy.getMatch(original, compare)
