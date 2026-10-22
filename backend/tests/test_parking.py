import datetime as real_dt

import pytest

import app.services.parking_service as ps_module
from app.models.parking import ParkingRecord


def test_duplicate_entry_is_rejected(service):
    """Entering a plate that is already parked (status IN) must be rejected."""
    service.create_parking_record("ABC123", 0.9)
    with pytest.raises(Exception, match="already parked"):
        service.create_parking_record("ABC123", 0.9)


def test_exit_without_record_is_rejected(service):
    """Exiting a plate with no active (status IN) record must be rejected."""
    with pytest.raises(Exception, match="No active parking record"):
        service.process_vehicle_exit("ABC123", 0.9)


def _create_entry_at(service, plate, entry_time):
    service.create_parking_record(plate, 0.9)
    rec = (
        service.db.query(ParkingRecord)
        .filter(ParkingRecord.plate_number == plate)
        .first()
    )
    rec.entry_time = entry_time
    service.db.commit()
    return rec


def test_billing_boundaries(service, monkeypatch):
    """Fee boundary behaviour: free up to 2h, then ceil() of the excess hours.

    Pricing rule under test: free_hours = 2.0, hourly_rate = 5.0.
    """
    fixed_now = real_dt.datetime(2026, 1, 1, 12, 0, 0)

    class FixedDatetime:
        @classmethod
        def now(cls, tz=None):
            return fixed_now

    monkeypatch.setattr(ps_module, "datetime", FixedDatetime)

    cases = [
        (real_dt.timedelta(hours=1), 0.0),               # within free period
        (real_dt.timedelta(hours=2), 0.0),               # exactly at free boundary
        (real_dt.timedelta(hours=2, minutes=1), 5.0),    # just over -> ceil to 1h
        (real_dt.timedelta(hours=3), 5.0),               # exactly 1 chargeable hour
        (real_dt.timedelta(hours=3, minutes=1), 10.0),   # rounds up to 2h
    ]

    for index, (offset, expected_fee) in enumerate(cases):
        plate = f"PLATE{index}"
        _create_entry_at(service, plate, fixed_now - offset)
        result = service.process_vehicle_exit(plate, 0.9)
        assert result["parking_fee"] == expected_fee
