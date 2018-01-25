
from chatterbot import ChatBot
import ip2region.ip2Region
gl_session={}
gl_rd = None
gl_chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

dbFile = 'ip2region/data/ip2region.db'
gl_ip_searcher = ip2region.ip2Region.Ip2Region(dbFile)
# Train based on the english corpus
#gl_chatbot.train("chatterbot.corpus.english")