from parsing.initconf import config, init_config
init_config()

from parsing.SiteLoader import *
parseAll(True)
#sl = SiteLoader("57")
#sl
from start.htmlLoader import htmltomd

htmltomd(57)
# "Страница не найдена 404"