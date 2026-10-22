"""Cross-page value guard: proposal section 11 rule 5 and section 16 criterion 3.

Inputs represent the same detected result in the same units. Agreement only
permits further review; this guard does not confirm results or save records.
"""

import re
from decimal import Decimal

import pytest
from pydantic_ai.models import override_allow_model_requests

from app import rules


@pytest.mark.parametrize(
    ('result_value', 'detection_value'),
    [('3.7', '3.7'), ('0.27', '0.270')],
)
def test_matching_page_values_pass_the_guard(
    result_value: str, detection_value: str,
) -> None:
    with override_allow_model_requests(False):
        rules.validate_page_values(
            result_value=Decimal(result_value),
            detection_value=Decimal(detection_value),
            result_page=10,
            detection_page=7,
        )


@pytest.mark.parametrize(
    ('result_value', 'detection_value', 'result_page', 'detection_page'),
    [('13.7', '3.7', 10, 7), ('3.7', '13.7', 12, 4)],
)
def test_conflicting_page_values_are_rejected_with_source_pages(
    result_value: str,
    detection_value: str,
    result_page: int,
    detection_page: int,
) -> None:
    message = (
        'Result not confirmed: values disagree between '
        f'page {detection_page} and page {result_page}'
    )
    with override_allow_model_requests(False), pytest.raises(
        ValueError, match=f'^{re.escape(message)}$',
    ):
        rules.validate_page_values(
            result_value=Decimal(result_value),
            detection_value=Decimal(detection_value),
            result_page=result_page,
            detection_page=detection_page,
        )
