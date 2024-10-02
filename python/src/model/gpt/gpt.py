import os
import subprocess
from openai import OpenAI
import json
from dotenv import load_dotenv
from speech.speech import SpeechRecog
from dao.filedao import FileDAO

load_dotenv()

class GPTProcessing:
    def __init__(self):
        self.speech = SpeechRecog()
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.file_dao = FileDAO()

        self.action_map = {
            "git_commit": self.commit_changes,
            "open_program": self.open_program,
            "send_web_page": self.send_web_page,
            "open_web_page": self.open_web_page
        }

        self.detailed_instruction = {
            "role": "system",
            "content": (
                "You are JARVIS, an AI assistant. You are rational, logical and slightly funny. "
                "When you address me, do so as Sir, just like JARVIS in Iron Man. "
                "Interpret the user's command and return a structured response in JSON format. "
                "Based on the user's input, identify the correct action and provide the relevant parameters in JSON format. "
                "Include a 'text_reply' field in the JSON that contains a normal response from you. "
                "NEVER use Code Blocks. ALWAYS reply in JSON format. "
                "Here are some examples:\n\n"
                "- For committing changes to a Git project (You will have to ask for the commit message):\n"
                "  User Input: 'Jarvis, commit my changes to project <name>'\n"
                "  Response: {\"action\": \"git_commit\", \"parameters\": {\"project\": \"<name>\"}, \"text_reply\": \"<Your response>\"}\n\n"
                "- For opening a program:\n"
                "  User Input: 'Jarvis, open <program name>'\n"
                "  Response: {\"action\": \"open_program\", \"parameters\": {\"program\": \"<program name>\"}, \"text_reply\": \"<Your response>\"}\n\n"
                "- For sending a web page to a device:\n"
                "  User Input: 'Jarvis, send this web page to my <device>'\n"
                "  Response: {\"action\": \"send_web_page\", \"parameters\": {\"url\": \"<Current URL>\", \"device\": \"<device>\"}, \"text_reply\": \"<Your response>\"}\n\n"
                "Provide the correct JSON based on the user's input."
            )
        }

    def send_prompt(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    
    def send_messages(self, messages):
        messages.insert(0, self.detailed_instruction)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return response.choices[0].message.content
    
    def commit_changes(self, project):
        projects = self.file_dao.get_project_list()
        messages = [{"role": "system", "content": f"Find the project {project} in the list of projects: {projects}. Return the correct item on the list that corresponds to the project."}]
        response = self.send_messages(messages)
        _, params, _ = self.process_response(response)
        project_name = params.get("project")

        commit_message = self.speech.run()
        print("ME: ", commit_message)
        messages = [{"role": "system", "content": f"Project: {project_name}. User provided the following commit message: '{commit_message}'. Read the message back and request confirmation. Return the commit message with punctuation."}]
        response = self.send_messages(messages)
        _, params, _ = self.process_response(response)
        self.say_reply(response)
        
        commit_message = params.get("commit_message")

        confirmation = self.speech.run()
        print("ME: ", confirmation)
        messages = [
            {"role": "system", "content": f"Project: {project_name}. User replied to a confirmation request. If the reply is positive the action should be 'yes', if negative the action should be 'no'."},
            {"role": "user", "content": confirmation}
        ]
        response = self.send_messages(messages)
        action, _, _ = self.process_response(response)

        if action.lower() == "yes":
            messages = [{"role": "system", "content": f"Project: {project_name}. User confirmed the commit message. Proceeding with the commit. Assume the commit was successful and reply accordingly."}]
            response = self.send_messages(messages)
            self.say_reply(response)
        else:
            while action.lower() != "yes":
                messages = [{"role": "system", "content": f"Project: {project_name}. User did not agree with the commit message. Request the message again and proceed accordingly."}]
                response = self.send_messages(messages)
                self.say_reply(response)

                commit_message = self.speech.run()
                print("ME: ", commit_message)
                messages = [{"role": "system", "content": f"Project: {project_name}. User provided the following commit message: '{commit_message}'. Read the message back and request confirmation. Return the commit message with punctuation."}]
                response = self.send_messages(messages)
                _, params, _ = self.process_response(response)
                self.say_reply(response)

                commit_message = params.get("commit_message")

                confirmation = self.speech.run()
                print("ME: ", confirmation)
                messages = [
                    {"role": "system", "content": f"Project: {project_name}. User replied to a confirmation request. If the reply is positive the action should be 'yes', if negative the action should be 'no'."},
                    {"role": "user", "content": confirmation}
                ]
                response = self.send_messages(messages)
                action, _, _ = self.process_response(response)

        try:
            os.chdir(self.file_dao.find_project(project_name))
            subprocess.run(f"git add . && git commit -m \"{commit_message}\" && git push", shell=True, check=True)
            return f"Changes committed with message: '{commit_message}'"
        except subprocess.CalledProcessError as e:
            return f"Error committing changes: {str(e)}"

    def is_git_repository(self, workspace_path):
        return os.path.exists(os.path.join(workspace_path, ".git"))

    def handle_command(self, command):
        messages = [
            {"role": "user", "content": command}
        ]

        response = self.send_messages(messages)
        try:
            action, parameters, reply = self.process_response(response)
            self.speech.speak_text(reply)
            if action in self.action_map:
                self.action_map[action](**parameters)
            else:
                messages = [{"role": "system", "content": "You received an invalid action. Respond accordingly."}]
                response = self.send_messages(messages)
                self.say_reply(response)
        except Exception as e:
            print(f"Error: {str(e)}")

    def open_program(self, program):
        try:
            subprocess.Popen(program)
            return f"Opening {program.capitalize()}"
        except Exception as e:
            return f"Error opening program: {str(e)}"
        
    def open_web_page(self, url):
        try:
            subprocess.Popen(["xdg-open", url])
            return f"Opening web page: {url}"
        except Exception as e:
            return f"Error opening web page: {str(e)}"
        
    def send_web_page(self, url, device):
        return f"Sending web page: {url} to {device}"
    
    def say_reply(self, response):
        _, _, reply = self.process_response(response)
        self.speech.speak_text(reply)
    
    def process_response(self, response):
        response_data = json.loads(response)
        action = response_data.get("action")
        parameters = response_data.get("parameters")
        text_reply = response_data.get("text_reply")
        return action, parameters, text_reply