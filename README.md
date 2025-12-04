<h1 align="center">rsstream</h1>
<p align="center"></p>rsstream is a TUI application for reading RRS feeds, built on Textual. 

### Features

- Easily add and remove RSS feed URLs.
- Renders article content using Markdown.
- Open the original article link in your default web browser.
- Saves the user config in a dot file.

### Keybinds

| Key | Action | Description |
| :--- | :--- | :--- |
| `q` | `quit` | Exit the application. |
| `a` | `add_feed` | Open a dialog to add a new RSS feed URL. |
| `d` | `remove_feed` | Remove the currently selected feed (must be a feed title, not an article). |
| `j` | `scroll_text_down` | Scroll the article content down. |
| `k` | `scroll_text_up` | Scroll the article content up. |
| `o` | `open_browser` | Open the link to the original article in the default web browser. |

As well as standard mouse/arrow keys/enter support.

### Developers

1. Get the requirements
```bash
pip install -r requirements.txt
```

2.  Run the application

    ```bash
    python src/main.py
    ```


### Commit Rules

- [chore] for maintenance, build process changes, tooling, etc.
- [docs] for documentation changes
- [feat] for features
- [fix] for bugfixes/optimizations. 