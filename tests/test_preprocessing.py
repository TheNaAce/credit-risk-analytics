import numpy as np
import pandas as pd

from src.preprocessing import clean_emp_length, clean_percentage, clean_term, prepare_feature_frame


def test_clean_percentage():
    assert clean_percentage("13.56%") == 13.56
    assert np.isnan(clean_percentage(None))


def test_clean_emp_length():
    assert clean_emp_length("< 1 year") == 0.5
    assert clean_emp_length("10+ years") == 10.0
    assert clean_emp_length("3 years") == 3.0


def test_prepare_feature_frame_parses_common_lending_club_fields():
    data = pd.DataFrame(
        {
            "int_rate": ["12.5%"],
            "emp_length": ["2 years"],
            "term": ["36 months"],
            "loan_status": ["Fully Paid"],
        }
    )
    features = prepare_feature_frame(data, ["int_rate", "emp_length", "term"])
    assert features.loc[0, "int_rate"] == 12.5
    assert features.loc[0, "emp_length"] == 2.0
    assert features.loc[0, "term"] == 36.0
