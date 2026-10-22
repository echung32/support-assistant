"""HTTP routes and page for the evidence tracer skeleton."""

from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.agent import PLACEHOLDER_RESPONSE, TraceResponse

app = FastAPI(title='Drinking Water Evidence Tracer')


class DocumentInput(BaseModel):
    page_text: str
    page_number: int
    publication_id: str
    batch: str
    laboratory: str
    report_level: str | None = None
    revision: str | None = None
    qualifier_definitions: dict[str, str] = Field(default_factory=dict)


class TraceRequest(BaseModel):
    search_type: Literal['sample', 'analyte']
    query: str = Field(min_length=1)
    documents: list[DocumentInput] = Field(default_factory=list)


@app.get('/', response_class=HTMLResponse)
def index() -> str:
    return Path(__file__).with_name('page.html').read_text(encoding='utf-8')


@app.post('/api/trace', response_model=TraceResponse)
def trace(request: TraceRequest) -> TraceResponse:
    """Return the same example for every valid request."""
    return PLACEHOLDER_RESPONSE
