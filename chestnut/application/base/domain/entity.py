class Entity:
    id: int | str

    def __eq__(self, __o: object) -> bool:
        return __o.id == self.id if isinstance(__o, type(self)) else False

    def __hash__(self) -> int:
        return hash(self.id)


class AggregateRoot(Entity):
    ...
