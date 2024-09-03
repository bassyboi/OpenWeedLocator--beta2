import os
import openai
from github import Github

# OpenAI GPT-4 setup
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(issue_title, issue_body):
    prompt = f"An issue was raised with the title: '{issue_title}'. The content is: '{issue_body}'. Provide a helpful and concise response to the issue."

    # Use the new `openai.ChatCompletion.create` method for GPT models
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    
    return response['choices'][0]['message']['content'].strip()

# GitHub setup
github_token = os.getenv('GH_TOKEN')  # Use the correct secret name 'GH_TOKEN'
if not github_token:
    raise ValueError("GitHub token not found in environment variables.")

g = Github(github_token)

repo_name = os.getenv('GITHUB_REPOSITORY')
if not repo_name:
    raise ValueError("GitHub repository not specified in environment variables.")

repo = g.get_repo(repo_name)

issue_number = os.getenv('ISSUE_NUMBER')
if not issue_number:
    raise ValueError("Issue number not specified in environment variables.")

issue = repo.get_issue(number=int(issue_number))

response = generate_response(issue.title, issue.body)

# Post response as a comment on the GitHub issue
issue.create_comment(response)
