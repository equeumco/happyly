from abc import ABC
from typing import Mapping, Any

from attr import attrs

from handling import Handler, HandlingResult
from listening import Message
from parsing.parser import Parser
from subscribing import Subscriber


@attrs(auto_attribs=True, frozen=True)
class Listener(ABC):
    handler: Handler
    parser: Parser
    subscriber: Subscriber

    def on_received(self, message: Message):
        pass

    def on_acknowledged(self, message: Message):
        pass

    def on_parsed(self, original: Message, parsed: Mapping[str, Any]):
        pass

    def on_parsing_failed(self, message: Message, error: Exception):
        raise error

    def on_handled(self, result: HandlingResult):
        pass

    def _actual_callback(self, message: Message):
        self.on_received(message)
        message.ack()
        try:
            parsed = self.parser.parse(message)
            self.on_parsed(original=message, parsed=parsed)
        except Exception as e:
            self.on_parsing_failed(message, e)
            return
        result = self.handler(parsed)
        self.on_handled(result)

    def start_listening(self):
        return self.subscriber.subscribe(callback=self._actual_callback)
