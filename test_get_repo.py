import unittest
from unittest.mock import patch, Mock
import requests

from get_repo import get_repos_and_commits




class TestGitHubAPI(unittest.TestCase):
    
    @patch('requests.get')
    def test_valid_user_with_repos(self, mock_get):
        # Mock response for repos list
        mock_repos_response = Mock()
        mock_repos_response.raise_for_status.return_value = None
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        
        # Mock response for commits count
        mock_commits_response = Mock()
        mock_commits_response.raise_for_status.return_value = None
        mock_commits_response.status_code = 200
        mock_commits_response.json.side_effect = [
            [{"sha": "commit1"}, {"sha": "commit2"}],  # 2 commits in repo1
            [{"sha": "commit1"}]                       # 1 commit in repo2
        ]

        # Assign the mocked responses to the requests.get calls
        mock_get.side_effect = [mock_repos_response, mock_commits_response, mock_commits_response]

        # Call the function
        result = get_repos_and_commits("valid_user")

        # Verify the results
        expected_result = [("repo1", 2), ("repo2", 1)]
        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_user_not_found(self, mock_get):
        # Mock response for user not found
        mock_get.return_value = Mock(status_code=404)

        # Call the function
        result = get_repos_and_commits("nonexistent_user")

        # Verify the results
        self.assertEqual(result, "User 'nonexistent_user' not found")

    @patch('requests.get')
    def test_valid_user_no_repos(self, mock_get):
        # Mock response for no repos
        mock_repos_response = Mock()
        mock_repos_response.raise_for_status.return_value = None
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = []  # No repositories

        mock_get.return_value = mock_repos_response

        # Call the function
        result = get_repos_and_commits("user_with_no_repos")

        # Verify the results
        self.assertEqual(result, [])

    @patch('requests.get')
    def test_commit_retrieval_error(self, mock_get):
        # Mock response for repos list
        mock_repos_response = Mock()
        mock_repos_response.raise_for_status.return_value = None
        mock_repos_response.status_code = 200
        mock_repos_response.json.return_value = [
            {"name": "repo1"}
        ]

        # Mock response for commit retrieval failure
        mock_commits_response = Mock()
        mock_commits_response.raise_for_status.side_effect = requests.exceptions.RequestException("Error retrieving commits")

        # Assign the mocked responses to the requests.get calls
        mock_get.side_effect = [mock_repos_response, mock_commits_response]

        # Call the function
        result = get_repos_and_commits("user_with_commit_error")

        # Verify the results
        expected_result = [("repo1", "Error retrieving commits: Error retrieving commits")]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
