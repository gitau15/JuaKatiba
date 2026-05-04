from pydantic import BaseModel, Field


class QueryFilters(BaseModel):
    org: str | None = None
    min_date: str | None = None
    notice_id: str | None = None


class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    tier: str = Field(default="public", pattern="^(public|enterprise)$")
    filters: QueryFilters | None = None


class IngestNoticeRequest(BaseModel):
    notice_id: str
    date: str
    ministry: str
    notice_type: str
    text: str = Field(min_length=30)
    entities_org: list[str] = Field(default_factory=list)


class Source(BaseModel):
    notice_id: str
    date: str


class QueryResponse(BaseModel):
    answer: str
    status: str = Field(pattern="^(ok|insufficient_context|blocked)$")
    sources: list[Source] = Field(default_factory=list)
    reason: str | None = None
