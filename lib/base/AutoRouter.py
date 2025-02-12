from pathlib import Path

from aiogram import Router, Bot
from aiogram.types import FSInputFile

from numpy import deprecate

from Utils.KeyboardMaker import button_text_back_to_main_menu_new

from lib.base.AutoNode import AutoNode, AutoNodeAnswerType
from lib.base.ExtraAutoNodes import ExtraAutoNodes


class AutoRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.node_dict: dict[str, AutoNode] = {}

    def _load_media(self, media: FSInputFile | Path | str | None) -> FSInputFile | None:
        if isinstance(media, str) or isinstance(media, Path):
            media = FSInputFile(media)
        return media

    def add_node(
        self,
        node: AutoNode,
    ) -> None:
        self.node_dict[node.node_name] = node

    def create_node(
        self,
        node_name: str,
        text: dict[str, str] | None = None,
        media: FSInputFile | Path | str | None = None,
        answer_type: AutoNodeAnswerType = AutoNodeAnswerType.NEW_MESSAGE,
        **node_message_kwargs,
    ) -> AutoNode:
        media = self._load_media(media)

        node = AutoNode(
            self.bot,
            self,
            node_name,
            text,
            media,
            answer_type=answer_type,
            **node_message_kwargs,
        )
        self.add_node(node)
        return node

    @deprecate(
        message=(
            "This is a workaround method, use add edge "
            "methods instead to make proper entry points "
            "for nodes"
        )
    )
    def convert_to_entry_node(
        self,
        node_name: str,
    ) -> None:
        assert node_name in self.node_dict, f"Node {node_name} doesn't exist"
        self.node_dict[node_name].register_callback_handler()

    def add_button_edge(
        self,
        node_name: str,
        next_node: str | ExtraAutoNodes,
        button_text: dict[str, str] | None = None,
        is_node_local: bool = True,
        is_next_node_local: bool = True,
    ) -> None:

        assert not is_node_local or node_name in self.node_dict, f"Node {node_name} doesn't exist"

        # Register required functions on destination node
        if is_next_node_local and not isinstance(next_node, ExtraAutoNodes) and not next_node.startswith(
            "http"
        ):
            assert next_node in self.node_dict, f"Node {next_node} doesn't exist"

            self.node_dict[next_node].register_callback_handler()

        if not is_node_local:
            return

        # Simplifing ExtraAutoNodes
        next_node_name: str
        if next_node == ExtraAutoNodes.HOME_NODE:
            next_node_name, button_text = button_text_back_to_main_menu_new
        elif isinstance(next_node, ExtraAutoNodes):
            next_node_name = next_node.value
        else:
            next_node_name = next_node

        assert (
            button_text is not None
        ), "Button text can't be None for edge with ordinary nodes"

        # Add edge
        self.node_dict[node_name].add_keyboard_button(next_node_name, button_text)

    def add_message_edge(
        self,
        node_name: str,
        next_node_name: str,
        state_destination: str | None = None,
        is_node_local: bool = True,
        is_next_node_local: bool = True,
    ) -> None:
        
        assert not is_node_local or node_name in self.node_dict, f"Node {node_name} doesn't exist"

        assert not is_node_local or not self.node_dict[
            node_name
        ].has_next_message_node, "Message handler already registered"

        assert is_next_node_local, f"Currently, nodes from different routers are not supported"

        endpoint = self.node_dict[next_node_name].register_message_handler(destination=state_destination)
        
        if is_node_local:
            self.node_dict[node_name].add_state_changer(endpoint)

    def add_selector_edge(
        self,
        node_name: str,
        next_node: str,
        selector: list[tuple[dict[str, str], str]],
        state_destination: str | None = None,
        is_node_local: bool = True,
        is_next_node_local: bool = True,
    ) -> None:
        assert not is_node_local or node_name in self.node_dict, f"Node {node_name} doesn't exist"

        endpoint: str | None = None

        # Register required functions on destination node
        if is_next_node_local:
            assert next_node in self.node_dict, f"Node {next_node} doesn't exist"
            assert not self.node_dict[next_node].has_callback_with_information_handler

            endpoint = self.node_dict[next_node].register_callback_with_information_handler(
                state_destination
            )
            
        if not is_node_local:
            return

        # Add edge
        for (button, value) in selector:
            self.node_dict[node_name].add_keyboard_button(f"{endpoint}:{value}", button)

    def reload_assets(self) -> None:
        pass
