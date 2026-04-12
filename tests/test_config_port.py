from app.config import Settings


def test_settings_prefers_railway_port_env(monkeypatch):
    monkeypatch.setenv("PORT", "9001")
    monkeypatch.setenv("AI_PORT", "8000")

    settings = Settings()

    assert settings.ai_port == 9001


def test_settings_falls_back_to_ai_port(monkeypatch):
    monkeypatch.delenv("PORT", raising=False)
    monkeypatch.setenv("AI_PORT", "8010")

    settings = Settings()

    assert settings.ai_port == 8010
