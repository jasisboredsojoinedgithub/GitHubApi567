import requests
import json

github_id = "jasisboredsojoinedgithub"

def get_repos_and_commits(github_id):
    if not github_id or not isinstance(github_id, str):
        raise ValueError("GitHub ID must be a non-empty string")

    results = []
    
    try:
        repos_url = f"https://api.github.com/users/{github_id}/repos"
        repos_response = requests.get(repos_url)

        if repos_response.status_code == 404:
            return f"User '{github_id}' not found"
        
        repos_response.raise_for_status()
        repos = repos_response.json()
        
        for repo in repos:
            repo_name = repo["name"]
            commits_url = f"https://api.github.com/repos/{github_id}/{repo_name}/commits"
            
            try:
                commits_response = requests.get(commits_url)
                commits_response.raise_for_status()
                commit_count = len(commits_response.json())
                results.append((repo_name, commit_count))
            except requests.exceptions.RequestException as e:
                results.append((repo_name, f"Error retrieving commits: {str(e)}"))
                
        return results
        
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to retrieve repository data: {str(e)}")

def display_repo_info(github_id):
    try:
        results = get_repos_and_commits(github_id)
        
        if isinstance(results, str):  
            print(results)
            return
            
        if not results:
            print(f"No repositories found for user '{github_id}'")
            return
            
        for repo_name, commit_count in results:
            if isinstance(commit_count, int):
                print(f"Repo: {repo_name} Number of commits: {commit_count}")
            else:
                print(f"Repo: {repo_name} {commit_count}")
                
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    display_repo_info(github_id)
