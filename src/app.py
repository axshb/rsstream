import webbrowser
from typing import Dict, Any

from textual.app import App, ComposeResult
from textual.widgets import Tree, Header, Footer, Markdown
from textual.containers import Container, VerticalScroll
from textual import work

# local imports
from config import load_config, save_config
from parser import fetch_feed_data
from screens import AddFeedScreen

class RsStream(App):
    CSS = """
    #main-layout { layout: horizontal; height: 100%; }
    #tree-container { width: 35%; height: 100%; border-right: solid $primary; }
    #content-container { width: 65%; height: 100%; }
    Markdown { padding: 1 2; }
    """

    BINDINGS = [
        ("q", "quit", "quit"),
        ("a", "add_feed", "add feed"),
        ("d", "remove_feed", "remove feed"),
        ("j", "scroll_text_down", "scroll down"),
        ("k", "scroll_text_up", "scroll up"),
        ("o", "open_browser", "open link"),
    ]

    # app state
    config_data: Dict[str, Any] = {}
    current_article_link: str = ""

    def on_mount(self) -> None:
        # load config/theme on startup
        self.config_data = load_config()
        self.theme = self.config_data.get("theme", "textual-dark")
        self.dark = self.config_data.get("dark_mode", True)
        self.refresh_feeds()

    def on_unmount(self) -> None:
        # save stuff before we die
        self.config_data["theme"] = self.theme
        self.config_data["dark_mode"] = self.dark
        save_config(self.config_data)

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main-layout"):
            with Container(id="tree-container"):
                tree = Tree("RSS Feeds", id="feed-tree")
                # turn off auto_expand so manual toggling feels better
                tree.auto_expand = False
                yield tree
            with VerticalScroll(id="content-container"):
                yield Markdown("Select an article...", id="article-content")
        yield Footer()

    @work(exclusive=True)
    async def refresh_feeds(self):
        # fetches feeds in a worker thread so UI doesn't freeze
        tree = self.query_one("#feed-tree", Tree)
        tree.clear()
        tree.root.expand()
        
        self.notify("Refreshing feeds...")
        
        feed_urls = self.config_data.get("feeds", [])
        
        for url in feed_urls:
            # this is blocking (requests/urllib) so it needs to be inside @work
            data = fetch_feed_data(url)
            
            for feed_title, items in data.items():
                feed_node = tree.root.add(feed_title, data={"type": "feed", "url": url})
                
                for label, info in items.items():
                    # stashing the whole article dict in the node data
                    feed_node.add_leaf(label, data={"type": "article", **info})
                
        self.notify("Feeds updated.", timeout=2)

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node = event.node
        if not node.data: return

        if node.data.get("type") == "article":
            self.display_article(node.data)
        elif node.data.get("type") == "feed":
            node.toggle()

    def display_article(self, data: Dict[str, Any]):
        content_display = self.query_one("#article-content", Markdown)
        scroll_container = self.query_one("#content-container", VerticalScroll)
        
        title = data.get("title", "No Title")
        content = data.get("content", "")
        link = data.get("link", "")
        self.current_article_link = link

        # build markdown string
        md_text = f"# {title}\n"
        if link:
            md_text += f"**[Read Original Article]({link})**\n"
        md_text += f"\n---\n\n{content}"

        content_display.update(md_text)
        # reset scroll to top for new articles
        scroll_container.scroll_home(animate=False)

    def action_add_feed(self):
        # callback for when modal closes
        def check_add(url: str | None):
            if url:
                if url not in self.config_data["feeds"]:
                    self.config_data["feeds"].append(url)
                    self.refresh_feeds()
                    self.notify(f"Added: {url}")
                else:
                    self.notify("Feed already exists.", severity="warning")
        
        self.push_screen(AddFeedScreen(), check_add)

    def action_remove_feed(self):
        tree = self.query_one("#feed-tree", Tree)
        node = tree.cursor_node
        
        # make sure we're actually on a feed node
        if node and node.data and node.data.get("type") == "feed":
            url_to_remove = node.data.get("url")
            if url_to_remove in self.config_data["feeds"]:
                self.config_data["feeds"].remove(url_to_remove)
                node.remove()
                self.notify(f"Removed: {url_to_remove}")
        else:
            self.notify("Select a Feed title to remove it.", severity="warning")

    def action_open_browser(self):
        if self.current_article_link:
            webbrowser.open(self.current_article_link)
            self.notify("Opening browser...")

    def action_scroll_text_down(self):
        self.query_one("#content-container", VerticalScroll).scroll_down()

    def action_scroll_text_up(self):
        self.query_one("#content-container", VerticalScroll).scroll_up()