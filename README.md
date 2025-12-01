## rsstream: A TUI RSS Reader

<h1 align="center">rsstream</h1>
<p align="center">
  <img src="https://img.shields.io/badge/Platform-Cross--Platform-blue.svg" alt="Platform">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/Python-3%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/github/last-commit/archiebhl/hwinsight.svg" alt="Last Commit">
</p>

rsstream is a simple **Terminal User Interface (TUI)** application for reading RSS feeds. It's built using the **Textual** TUI framework for Python.

### Features

  - **TUI Interface:** Read feeds directly in your terminal.
  - **Asynchronous Feed Fetching:** Uses Textual's `@work` decorator to fetch feeds in the background, keeping the UI responsive.
  - **Feed Management:** Easily add and remove RSS feed URLs.
  - **Article Display:** Renders article content using Markdown.
  - **Browser Integration:** Open the original article link in your default web browser.
  - **Configuration:** Saves feed list, theme, and dark mode preference automatically.

### Requirements

This application requires the dependencies listed in `requirements.txt`.

To install the necessary packages, use:

```bash
pip install -r requirements.txt
```

### Usage

1.  **Run the application:**

    ```bash
    python src/main.py
    ```

2.  **Navigation and Actions:** The application uses key bindings for interaction, which are also displayed in the footer.

| Key | Action | Description |
| :--- | :--- | :--- |
| `q` | `quit` | Exit the application. |
| `a` | `add_feed` | Open a dialog to add a new RSS feed URL. |
| `d` | `remove_feed` | Remove the currently selected feed (must be a feed title, not an article). |
| `j` | `scroll_text_down` | Scroll the article content down. |
| `k` | `scroll_text_up` | Scroll the article content up. |
| `o` | `open_browser` | Open the link to the original article in the default web browser. |
| **Mouse/Arrows** | **Select** | Navigate and select feed titles or articles in the left panel (Tree). |

### Contributing

Please adhere to the following simple commit conventions.

#### Commit Rules

Commits should be prefixed with a tag in square brackets indicating the type of change, followed by a concise description.

| Tag | Description | Example |
| :--- | :--- | :--- |
| `[chore]` | Maintenance, build process changes, tooling, etc. | `[chore] Update dependencies in requirements.txt` |
| `[docs]` | Documentation changes only. | `[docs] Clarify usage instructions in README` |
| `[feat]` | A new feature. | `[feat] Add support for filtering articles` |
| `[fix]` | A bug fix. | `[fix] Correct error handling in fetch_feed_data` |