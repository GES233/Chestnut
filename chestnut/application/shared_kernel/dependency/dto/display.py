from pydantic import BaseModel

from ....base.dto.io import OutputSchemaMixin


class DependentItem(OutputSchemaMixin, BaseModel):
    ...
