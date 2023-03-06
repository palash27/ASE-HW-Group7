def sym(n=0,s=""):
  """
  -- Create a `SYM` to summarize a stream of symbols.
  """
  return {
  'at': n,
  'txt': s,
  'n': 0,
  'mode': None,
  'most': 0,
  'isSym': True,
  'has': {}
  }