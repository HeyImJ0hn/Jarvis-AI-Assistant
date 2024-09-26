import os
import subprocess
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

class GPTProcessing:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def send_prompt(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    
    def send_messages(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return response.choices[0].message.content
    
    def commit_changes(self, workspace_path, commit_message):
        try:
            os.chdir(workspace_path)
            subprocess.run(['git', 'add', '.'], check=True)  
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)  
            return f"Changes committed with message: '{commit_message}'"
        except subprocess.CalledProcessError as e:
            return f"Error committing changes: {str(e)}"
        
    def get_current_workspace(self):
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith('.code-workspace'):
                    workspace_file_path = os.path.join(root, file)
                    print(f"Multi-root workspace found: {workspace_file_path}")
                    with open(workspace_file_path, 'r') as f:
                        workspace_data = json.load(f)
                        if 'folders' in workspace_data:
                            return os.path.abspath(workspace_data['folders'][0]['path'])
        print("Single-folder workspace detected.")
        return os.getcwd()
    
    def is_git_repository(self, workspace_path):
        return os.path.exists(os.path.join(workspace_path, ".git"))

    def handle_command(self, command):
        if command.lower() == "jarvis, commit my changes":
            messages = [
                {"role": "system", "content": "You are JARVIS, an AI assistant that helps the user with various tasks. You are rational, logic and slightly funny."},
                {"role": "user", "content": "I want to commit my changes. Please ask for a summary of the changes."}
            ]
            
            chat_response = self.send_messages(messages)
            print("JARVIS:", chat_response)
            
            user_summary = input("You: ")
            
            messages.append({"role": "user", "content": user_summary})
            confirmation_prompt = f"User provided a summary: '{user_summary}'. Ask them to confirm if they want to commit with this message."
            messages.append({"role": "assistant", "content": confirmation_prompt})

            confirmation_response = self.send_messages(messages)
            print("JARVIS:", confirmation_response)
            
            user_confirmation = input("You (yes/no): ") 
            
            if user_confirmation.lower() in ["yes", "y"]:
                workspace_path = self.get_current_workspace()
                if self.is_git_repository(workspace_path):
                    commit_response = self.commit_changes(workspace_path, user_summary)
                    print("JARVIS:", commit_response)
                else:
                    print("JARVIS: This workspace is not a Git repository.")
            else:
                print("JARVIS: Commit canceled.")
        else:
            messages = [{"role": "system", "content": "You are JARVIS, an AI assistant that helps the user with various tasks. You are rational, logic and slightly funny."},
                        {"role": "user", "content": command}]
            response = self.send_messages(messages)
            print("JARVIS:", response)

while True:
    gpt = GPTProcessing()
    user_input = input("You: ")
    gpt.handle_command(user_input)


