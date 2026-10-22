"""Plain Python checks for drinking water evidence."""

from decimal import Decimal


def validate_page_values(
    *,
    result_value: Decimal,
    detection_value: Decimal,
    result_page: int,
    detection_page: int,
) -> None:
    """Reject conflicting values for the same detected result in the same units.

    Matching values may proceed to review; agreement does not confirm a result.
    """
    if result_value != detection_value:
        raise ValueError(
            'Result not confirmed: values disagree between '
            f'page {detection_page} and page {result_page}'
        )
