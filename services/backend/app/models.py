from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    tier: str = Field(default="public", pattern="^(public|enterprise)$")


class Source(BaseModel):
    notice_id: str
    date: str


class QueryResponse(BaseModel):
    answer: str
    status: str = Field(pattern="^(ok|insufficient_context)$")
    sources: list[Source] = Field(default_factory=list)
