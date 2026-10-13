from src.metrics import ks_statistic


def test_ks_statistic_perfect_separation():
    y_true = [0, 0, 1, 1]
    y_score = [0.1, 0.2, 0.8, 0.9]
    assert ks_statistic(y_true, y_score) == 1.0


def test_ks_statistic_is_between_zero_and_one():
    value = ks_statistic([0, 1, 0, 1], [0.2, 0.3, 0.4, 0.5])
    assert 0 <= value <= 1
