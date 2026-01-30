import webbrowser
from typing import Dict, Any
import logging
import asyncio

from textual.app import App, ComposeResult
from textual.widgets import Tree, Header, Footer, Markdown
from textual.containers import Container, VerticalScroll
from textual import work
from textual.message import Message

from config import load_config, save_config
from parser import fetch_feed_data
from screens import AddFeedScreen

logger = logging.getLogger(__name__)

class FeedFetched(Message):
    def __init__(self, url: str, data: dict):
        self.url = url
        self.data = data
        super().__init__()

class RsStream(App):
    CSS = """
    #main-layout { layout: horizontal; height: 100%; }
    #tree-container { width: 35%; height: 100%; border-right: solid $primary; }
    #content-container { width: 65%; height: 100%; }
    Markdown { padding: 1 2; }
    """

    BINDINGS = [
        ("q", "quit", "quit"),
        ("a", "add_feed", "add"),
        ("d", "remove_feed", "remove"),
        ("j", "scroll_text_down", "down"),
        ("k", "scroll_text_up", "up"),
        ("o", "open_browser", "open"),
    ]

    def __init__(self):
        super().__init__()
        self.config_data: Dict[str, Any] = {}
        self.current_article_link: str = ""

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main-layout"):
            with Container(id="tree-container"):
                yield Tree("RSS Feeds", id="feed-tree")
            with VerticalScroll(id="content-container"):
                yield Markdown("Select an article...", id="article-content")
        yield Footer()

    async def on_mount(self) -> None:
        self.config_data = load_config()
        self.theme = self.config_data.get("theme", "textual-dark")
        self.dark = self.config_data.get("dark_mode", True)
        
        self.feed_tree = self.query_one("#feed-tree", Tree)
        self.feed_tree.root.expand()
        
        self.load_all_feeds()

    def on_unmount(self) -> None:
        self.config_data["theme"] = self.theme
        self.config_data["dark_mode"] = self.dark
        save_config(self.config_data)

     # unified fetcher for both startup and adding new feeds
    @work(thread=True)
    def load_all_feeds(self, url=None):
        if not url:
            urls = self.config_data.get("feeds", [])
        else:
            urls = [url]
        for url in urls:
            try:
                data = fetch_feed_data(url)
                self.post_message(FeedFetched(url, data))
            except Exception as e:
                logger.error(f"Error: {e}")

    # ui updating for feeds, called internally by message
    def on_feed_fetched(self, msg: FeedFetched):
        for feed_title, items in msg.data.items():
            feed_node = self.feed_tree.root.add(
                feed_title, 
                data={"type": "feed", "url": msg.url}
            )
            for label, info in items.items():
                feed_node.add_leaf(label, data={"type": "article", **info})

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node = event.node
        if not node.data: 
            return

        if node.data.get("type") == "article":
            self.display_article(node.data)
        elif node.data.get("type") == "feed":
            node.toggle()

    def display_article(self, data: Dict[str, Any]):
        self.current_article_link = data.get("link", "")
        md_text = f"# {data.get('title', 'No Title')}\n"
        if self.current_article_link:
            md_text += f"**[Read Original Article]({self.current_article_link})**\n"
        md_text += f"\n---\n\n{data.get('content', '')}"

        self.query_one("#article-content", Markdown).update(md_text)
        self.query_one("#content-container", VerticalScroll).scroll_home(animate=False)

    def action_add_feed(self):
        def handle_new_feed(url: str | None):
            if url and url not in self.config_data["feeds"]:
                self.config_data["feeds"].append(url)
                self.load_all_feeds(url)
                self.notify(f"added {url}")
        
        self.push_screen(AddFeedScreen(), handle_new_feed)

    def action_remove_feed(self):
        node = self.feed_tree.cursor_node
        if node and node.data and node.data.get("type") == "feed":
            url = node.data.get("url")
            if url in self.config_data["feeds"]:
                self.config_data["feeds"].remove(url)
                node.remove()
                self.notify(f"removed {url}")
        else:
            self.notify("select a feed title to remove", severity="warning")

    def action_open_browser(self):
        if self.current_article_link:
            webbrowser.open(self.current_article_link)

    def action_scroll_text_down(self):
        self.query_one("#content-container", VerticalScroll).scroll_down()

    def action_scroll_text_up(self):
        self.query_one("#content-container", VerticalScroll).scroll_up()