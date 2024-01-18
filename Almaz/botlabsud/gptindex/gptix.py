from gptindex.ixapp import ixapp
from conf import config

ixapp.config.index_path = config.index_path
ixapp.config.OPENAI_API_KEY = config.OPENAI_API_KEY


