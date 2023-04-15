from pydantic import BaseModel

from ....core.dto.io import OutputSchemaMixin


class DependentItem(OutputSchemaMixin, BaseModel):
    ...
