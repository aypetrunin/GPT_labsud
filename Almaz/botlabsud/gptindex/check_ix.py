from gptix import ixapp
from gptindex.gptutils import *
ixapp.init()
print(ixapp.promt, num_tokens_from_string(ixapp.promt))
