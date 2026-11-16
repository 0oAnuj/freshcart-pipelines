from sklearn.datasets import load_iris
from iris_project.transformers.prepare_data import prepare_data

def test_split_is_80_20():
    df = load_iris(as_frame=True).frame
    out = prepare_data(df)

    assert (out["split"] == "train").sum() == 120
    assert (out["split"] == "test").sum() == 30


def test_prepare_data_preserves_all_rows():
    df = load_iris(as_frame=True).frame
    out = prepare_data(df)

    assert len(out) == len(df)


def test_prepare_data_assigns_only_train_and_test_labels():
    df = load_iris(as_frame=True).frame
    out = prepare_data(df)

    assert set(out["split"]) == {"train", "test"}


def test_prepare_data_split_labels_are_non_empty():
    df = load_iris(as_frame=True).frame
    out = prepare_data(df)

    assert out["split"].notna().all()
