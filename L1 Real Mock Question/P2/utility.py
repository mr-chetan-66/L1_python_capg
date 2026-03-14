# utility.py
from exception import InvalidRequestIdException
import re
from datetime import datetime
from datetime import date as date_cls
from typing import List


def convert_date(str_date: str) -> date_cls:
    return datetime.strptime(str_date.strip(), "%Y-%m-%d").date()


def validate_request_id(request_id: str) -> bool:
    if not isinstance(request_id, str) or len(request_id.strip()) < 4:
        raise InvalidRequestIdException("Invalid Request Id")
    if not re.fullmatch(r"R00\d+", request_id.strip()):
        raise InvalidRequestIdException("Invalid Request Id")
    return True


def _is_approved(val: str) -> bool:
    if val is None:
        return False
    v = val.strip().lower()
    return v in {"approved", "approve", "yes", "y", "true", "t", "1"}


def read_file(filename: str) -> List[str]:
    records = []
    with open(filename) as f:
        for row in f:
            if not row.strip():
                continue
            # Pad/truncate to 13 fields defensively
            lst=row.split(",")
            dor=lst[2]
            dot=lst[4]
            approval=lst[7]

            try:
                # Filter: approval & 180-day window
                if not _is_approved(approval):
                    continue
                d_req = convert_date(dor)
                d_trv = convert_date(dot)
                delta = (d_req - d_trv).days
                if delta < 0 or delta > 180:
                    continue
                # Keep the original comma-separated record line
                records.append(row)
            except Exception:
                # If any parsing fails for this row, skip it silently
                continue
    return records
