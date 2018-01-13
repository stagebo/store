from chatterbot import ChatBot

chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus
# chatbot.train("chatterbot.corpus.english")

# Get a response to an input statement
print("start")
t=chatbot.get_response("i want to suicide")
print(t)
print(chatbot.get_response("who is the most beautiful woman?"))
print(chatbot.get_response("who is the most beautiful man?"))
print(chatbot.get_response("where are you?"))
print(chatbot.get_response("would you like some tee to drink?"))

print(chatbot.get_response("what's your name?"))