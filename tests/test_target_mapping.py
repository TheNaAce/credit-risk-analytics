import pandas as pd

from src.target import add_default_target, map_loan_status_to_default


def test_known_status_mapping():
    assert map_loan_status_to_default("Fully Paid") == 0
    assert map_loan_status_to_default("Charged Off") == 1
    assert map_loan_status_to_default("Default") == 1
    assert map_loan_status_to_default("Current") is None


def test_add_default_target_excludes_current_loans():
    data = pd.DataFrame({"loan_status": ["Fully Paid", "Charged Off", "Current"]})
    mapped = add_default_target(data)
    assert mapped["default_flag"].tolist() == [0, 1]
