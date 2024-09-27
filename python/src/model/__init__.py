from gpt.gpt import GPTProcessing
from speech.speech import SpeechRecog

while True:
    gpt = GPTProcessing()
    speech = SpeechRecog()
    user_input = speech.run()
    print("ME: ", user_input)
    if user_input == None:
        speech.speak_text("Sorry, could you say that again?")
    else:
        gpt.handle_command(user_input)

    '''
    gpt = GPTProcessing()
    user_input = input("YOU: ")
    print("ME: ", user_input)
    gpt.handle_command(user_input)
    '''
