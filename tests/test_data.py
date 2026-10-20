from src.data import clean as clean_module
from src.data import download as download_module


class _FakeResponse:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        pass


def test_download_saves_raw_csv(tmp_path, monkeypatch):
    sample_row = "63.0,1.0,1.0,145.0,233.0,1.0,2.0,150.0,0.0,2.3,3.0,0.0,6.0,0"

    def fake_get(url, timeout):
        return _FakeResponse(sample_row)

    monkeypatch.setattr(download_module.requests, "get", fake_get)

    output_path = tmp_path / "heart_disease.csv"
    result_path = download_module.download(output_path)

    assert result_path == output_path
    assert output_path.exists()
    content = output_path.read_text()
    assert content.splitlines()[0] == ",".join(download_module.COLUMNS)
    assert sample_row in content


def test_clean_removes_missing_and_binarizes_target(tmp_path):
    raw_csv = tmp_path / "raw.csv"
    raw_csv.write_text(
        "age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target\n"
        "63,1,1,145,233,1,2,150,0,2.3,3,0,6,0\n"
        "67,1,4,160,286,0,2,108,1,1.5,2,3,3,2\n"
        "57,0,4,120,354,0,0,163,1,0.6,1,?,3,0\n"
    )
    output_csv = tmp_path / "clean.csv"

    df = clean_module.clean(raw_csv, output_csv)

    assert output_csv.exists()
    assert not df.isna().any().any()
    assert set(df["target"].unique()) <= {0, 1}
    assert len(df) == 2  # the row with "?" in ca is dropped
