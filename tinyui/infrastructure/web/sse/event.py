from dataclasses import dataclass
from typing import Iterable, List, Any


@dataclass
class EventItem:
    id: int | None
    event_type: str | None
    retry: int | None
    data: Iterable[Any] | None

    def text(self) -> str:
        response = "\n".join([f"id: {self.id}", f"event: {self.event_type}\n"])

        if self.retry:
            response += f"retry: {int(self.retry)}\n"
        if self.data:
            response += "".join(["data: " + item + "\n" for item in self.data])
            return response

        raise NotImplementedError

    @classmethod
    def event(
        cls,
        id: int | None = None,
        event_type: str | None = None,
        retry: int | None = None,
        data: Iterable[Any] | None = None,
    ) -> str:
        item = EventItem(id=id, event_type=event_type, retry=retry, data=data)
        return item.text()
