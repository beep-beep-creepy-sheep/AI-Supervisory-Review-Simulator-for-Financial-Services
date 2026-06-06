from src.reporting.generate_report import run_pipeline


def test_report_generation_smoke():
    outputs = run_pipeline()
    assert outputs["evidence_pack"].exists()
    assert outputs["dashboard_data"].exists()
    assert outputs["supervisory_letter"].exists()
    assert outputs["risk_register"].exists()
    assert outputs["dashboard_data"].name == "dashboard_data.json"
    assert outputs["public_data"].exists()
