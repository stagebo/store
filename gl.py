
from chatterbot import ChatBot

gl_session={}
gl_rd = None
gl_chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)
# Train based on the english corpus
#gl_chatbot.train("chatterbot.corpus.english")