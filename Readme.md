# GitHub Collaborator Management Tool

This Python script helps you manage collaborators in your GitHub repositories across multiple organizations. It allows you to either list the repositories where a user is a collaborator or to remove that user. It supports both interactive removal with confirmation, and forceful removal without confirmation.

## Features

*   **List Collaborator Repositories:** Quickly find out which repositories a user has access to.
*   **Interactive Removal:** Remove a collaborator from specific repositories after getting a user confirmation prompt for each repo.
*   **Forceful Removal:** Remove a collaborator from all repositories without user interaction or confirmation using `--deleteforcefull` flag (use with extreme caution!).
*   **Organization Support:** Works across all organizations that you own or have admin rights in.
*   **Environment Variable Security:** Uses environment variables to keep your GitHub Personal Access Token secure.
*   **Rate Limit Handling:** Implements basic rate limit handling to avoid being blocked by the GitHub API.
*   **Clear Usage Instructions:** Provides clear instructions and examples when run with incorrect arguments.

## Prerequisites

*   **Python 3.6 or higher:**  Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).
*   **`requests` Library:** Install the required Python library using `pip install -r requirements.txt` (see below).
*   **GitHub Personal Access Token (PAT):** You'll need a PAT with the `repo`, and `admin:org` scopes. You can generate one in your GitHub settings under "Developer settings" -> "Personal access tokens".
*    **`.env` File:** Create a `.env` file at the same location of this script and set the `GITHUB_TOKEN` with your Personal Access Token.

## Setup

1.  **Clone the Repository:** Clone this repository to your local machine, or download the `script.py` file and `requirements.txt` to your local machine.
2.  **Create `.env` File:** Create a file named `.env` in the same directory as your script. Add your GitHub personal access token there as:
    ```
    GITHUB_TOKEN=your_actual_github_personal_access_token
    ```
    **Important:** Replace `your_actual_github_personal_access_token` with your generated PAT.
3.  **Install Dependencies:** Navigate to the directory containing the script and run the following command to install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The script provides three modes of operation:

1.  **List Collaborator Repositories:** To list the repositories where a user is a collaborator, run the script like this:

    ```bash
    python github_collaborator_manager.py <USERNAME>
    ```

    Replace `<USERNAME>` with the GitHub username of the user you want to check.

2.  **Remove Collaborator with User Confirmation:** To remove a user from specific repositories after getting a confirmation prompt for each, use the `--delete` flag:

    ```bash
    python github_collaborator_manager.py <USERNAME> --delete
    ```

    Replace `<USERNAME>` with the username of the user you wish to remove. The script will ask for confirmation before removing from each repo.

3.  **Forcefully Remove Collaborator Without Confirmation:** To forcefully remove a user from *all* repositories without any confirmation, use the `--deleteforcefull` flag:

    ```bash
    python github_collaborator_manager.py <USERNAME> --deleteforcefull
    ```
    
    **WARNING:** Use this option with *extreme caution*. It will immediately remove the user from all found repos and this action cannot be easily undone. It is recommended to use this only if you are sure and verified that user needs to be removed from every single repo.

## Examples

*   To check the repositories where `testuser` is a collaborator:
    ```bash
    python github_collaborator_manager.py testuser
    ```
*   To remove `testuser` from all listed repositories but prompt for confirmation before deleting:

    ```bash
    python github_collaborator_manager.py testuser --delete
    ```

*   To forcefully remove `testuser` from all repos without confirmation:

    ```bash
     python github_collaborator_manager.py testuser --deleteforcefull
    ```

## Notes

*   The script uses environment variables to store the GitHub token, which is the recommended way to handle sensitive credentials.
*   Make sure the `.env` file is in the same directory as your Python script, and the variable name should be exactly `GITHUB_TOKEN`.
*   The script has basic rate limit handling. It may slow down when dealing with many organizations or repositories.
*   The script will not check for ownership or if the user has access to remove the collaborators, make sure you have correct access rights before executing the script.

## Disclaimer

Use this script with caution. It has the potential to modify access to your repositories, so be sure to use the appropriate flag as needed. Especially, use the `--deleteforcefull` option with extreme caution. Always make sure the username you provide is correct.

## Contributing

Feel free to submit issues or pull requests if you find any bugs or want to add improvements.

## License

[Choose a license, or omit if you are not sure]