from enum import Enum
from typing import Callable, Coroutine, Any

from aiogram import Router, Bot
from aiogram.types import FSInputFile, User
from aiogram.fsm.context import FSMContext
from numpy import deprecate

from Utils.KeyboardMaker import button_text_back_to_main_menu_new

from lib.base.AutoNode import AutoNode, AutoNodeAnswerType


class ExtraAutoNodes(Enum):
    HOME_NODE = "home_node"


class AutoRouter(Router):
    def __init__(self, bot: Bot) -> None:
        super().__init__()

        self.bot = bot

        self.node_dict: dict[str, AutoNode] = {}

    def add_node(
        self,
        node_name: str,
        text: dict[str, str] | None = None,
        media: FSInputFile | str | None = None,
        answer_type: AutoNodeAnswerType = AutoNodeAnswerType.NEW_MESSAGE,
        node_trigger_callback: (
            Callable[
                [AutoNode, FSMContext, User | None, str | None],
                Coroutine[Any, Any, bool | None],
            ]
            | None
        ) = None,
        **node_message_kwargs,
    ) -> AutoNode:
        if isinstance(media, str):
            media = FSInputFile(media)

        node = AutoNode(
            self.bot,
            self,
            node_name,
            text,
            media,
            answer_type=answer_type,
            node_trigger_callback=node_trigger_callback,
            **node_message_kwargs,
        )
        self.node_dict[node_name] = node
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
    ) -> None:

        assert node_name in self.node_dict, f"Node {node_name} doesn't exist"

        # Register required functions on destination node
        if not isinstance(next_node, ExtraAutoNodes) and not next_node.startswith(
            "http"
        ):
            assert next_node in self.node_dict, f"Node {next_node} doesn't exist"

            self.node_dict[next_node].register_callback_handler()

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

    def add_message_edge(self, node_name: str, next_node_name: str) -> None:

        assert not self.node_dict[
            node_name
        ].has_next_message_node(), "Message handler already registered"

        self.node_dict[node_name].add_state_changer(
            self.node_dict[next_node_name].get_node_state()
        )
        self.node_dict[next_node_name].register_message_handler()
