"""Response schemas for the placeholder API; no agent is initialized."""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class SourcePage(BaseModel):
    publication_id: str
    page_number: int


class ScreeningLevel(BaseModel):
    value: Decimal
    units: str
    type: str
    source: SourcePage


class SampleDetails(BaseModel):
    field_sample_id: str
    location_id: str
    address: str
    latitude: float | None = None
    longitude: float | None = None
    flushing_zone: str
    collection_date: date
    collection_time: str | None = None
    sample_type: str | None = None
    requested_analyses: list[str] = Field(default_factory=list)
    batch_count: int


class InventoryItem(BaseModel):
    analyte: str
    method: str
    batch: str
    category: str


class Result(BaseModel):
    field_sample_id: str
    lab_sample_id: str | None = None
    analyte: str
    method: str
    batch: str
    result_as_written: str
    value: Decimal | None
    units: str
    qualifier: str | None
    reporting_limit: Decimal | None
    detection_limit: Decimal | None
    dilution: Decimal | None = None
    analysis_date: date | None = None
    source_pages: list[SourcePage]
    review_status: str
    unclear: bool
    validation_status: str
    summary_value: str | None
    status: str
    screening_levels: list[ScreeningLevel] = Field(default_factory=list)


class ValidationFinding(BaseModel):
    samples: list[str]
    analytes: list[str]
    qualifier: str
    reason: str
    source_page: SourcePage


class ReviewDecision(BaseModel):
    action: Literal['confirm', 'correct', 'flag']
    corrected_value: Decimal | None = None
    note: str
    reviewer: str
    timestamp: datetime
    result_index: int


class EvidenceSet(BaseModel):
    name: str
    selection: str
    included_results: list[int]
    export_date: date | None = None


class TraceResponse(BaseModel):
    placeholder: bool
    message: str
    sample: SampleDetails
    inventory: list[InventoryItem]
    results: list[Result]
    validation_findings: list[ValidationFinding]
    review_decisions: list[ReviewDecision]
    evidence_sets: list[EvidenceSet]


PLACEHOLDER_RESPONSE = TraceResponse(
    placeholder=True,
    message='Fixed demonstration data. No search, extraction, or comparison was performed.',
    sample=SampleDetails(
        field_sample_id='220113-I1-HT03', location_id='I1-MADR1832',
        address='1832 Madrona Place', flushing_zone='I1',
        collection_date=date(2022, 1, 13), batch_count=4,
        requested_analyses=['SVOCs', 'Metals', 'VOCs'],
    ),
    inventory=[InventoryItem(
        analyte='Lead', method='EPA 200.8', batch='2A14029', category='Estimated (J)',
    )],
    results=[Result(
        field_sample_id='220113-I1-HT03', analyte='Lead', method='EPA 200.8',
        batch='2A14029', result_as_written='0.27 J', value=Decimal('0.27'),
        units='µg/L', qualifier='J', reporting_limit=Decimal('0.50'),
        detection_limit=Decimal('0.088'),
        source_pages=[SourcePage(publication_id='pub_002925', page_number=10)],
        review_status='Unconfirmed demo', unclear=False,
        validation_status='None (demo)', summary_value='0.270',
        status='qualifier dropped (fixed example)',
    )],
    validation_findings=[], review_decisions=[],
    evidence_sets=[EvidenceSet(
        name='HT03 metals (demo)', selection='220113-I1-HT03', included_results=[0],
    )],
)
