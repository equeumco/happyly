from typing import Any, Mapping, Optional

from happyly.caching.cacher import Cacher
from happyly.handling import HandlingResult


class CacheByRequestIdMixin:
    def __init__(self, cacher: Cacher):
        self.cacher = cacher

    def on_received(self, message: Any):
        super().on_received(message)

        try:
            req_id = self._get_req_id(message)
        except Exception:
            pass
        else:
            self.cacher.add(message, key=req_id)

    def _get_req_id(self, message: Any) -> str:
        assert self.deserializer is not None

        attribtues = self.deserializer.deserialize(message)
        return attribtues[self.deserializer.request_id_field]

    def _rm(self, parsed_message: Mapping[str, Any]):
        assert self.deserializer is not None
        self.cacher.remove(parsed_message[self.deserializer.request_id_field])

    def on_published(
        self,
        original_message: Any,
        parsed_message: Optional[Mapping[str, Any]],
        result: HandlingResult,
    ):
        super().on_published(original_message, parsed_message, result)
        if parsed_message is not None:
            self._rm(parsed_message)

    def on_publishing_failed(
        self,
        original_message: Any,
        parsed_message: Optional[Mapping[str, Any]],
        result: HandlingResult,
        error: Exception,
    ):
        super().on_publishing_failed(original_message, parsed_message, result, error)
        if parsed_message is not None:
            self._rm(parsed_message)

    def on_deserialization_failed(self, message: Any, error: Exception):
        super().on_deserialization_failed(message, error)

        try:
            req_id = self._get_req_id(message)
        except Exception:
            pass
        else:
            self.cacher.remove(key=req_id)