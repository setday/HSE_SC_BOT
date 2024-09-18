import random
import pickle

from typing import Any, Optional

from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage


class BotStorage():
    instance: "BotStorage | None" = None
    request_dict: dict[int, list] = {}

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(BotStorage, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        pass
    
    def unload_data(self, dp : Dispatcher) -> None:
        try:
            with open("Data/request_dict.pickle", "wb") as f:
                pickle.dump(self.request_dict, f)

            if dp is None:
                print("No dispatcher found")
                return
            
            with open("Data/user_storage.pickle", "wb") as f:
                pickle.dump(dp.storage, f)
            print("Data unloaded")
        except Exception as e:
            print(f"Error while unloading data: {e}")

    def load_data(self) -> None:
        try:
            with open("Data/request_dict.pickle", "rb") as f:
                self.request_dict = pickle.load(f)
        except FileNotFoundError:
            print("No data found. Creating new storage...")

    def load_storage(self) -> BaseStorage | None:
        try:
            with open("Data/user_storage.pickle", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("No data found. Creating new storage...")
            return None
        
    def add_request(self, request: Any, request_id: Optional[int] = None) -> int:
        request_id = request_id or random.randint(1, 999999999)

        if request_id not in self.request_dict:
            self.request_dict[request_id] = []
        self.request_dict[request_id].append(request)

        return request_id

    def get_request(self, request_id: int) -> Any:
        if len(self.request_dict.get(request_id, [])) == 0:
            raise ValueError("No request found")
        return self.request_dict[request_id][-1]
