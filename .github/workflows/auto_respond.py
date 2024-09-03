import os
import openai
from github import Github

# OpenAI GPT-4 setup
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(issue_title, issue_body):
    prompt = f"An issue was raised with the title: '{issue_title}'. The content is: '{issue_body}'. Provide a helpful and concise response to the issue."
    
    response = openai.Completion.create(
      model="gpt-4",
      prompt=prompt,
      max_tokens=150,
      temperature=0.7
    )
    
    return response.choices[0].text.strip()

# GitHub setup
github_token = os.getenv('GITHUB_TOKEN')
g = Github(github_token)
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
issue_number = int(os.getenv('ISSUE_NUMBER'))

issue = repo.get_issue(number=issue_number)
response = generate_response(issue.title, issue.body)

# Post response as a comment on the GitHub issue
issue.create_comment(response)
