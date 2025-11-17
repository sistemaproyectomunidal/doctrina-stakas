import importlib.util
from pathlib import Path


def load_main_module(service_name: str):
    repo_root = Path(__file__).resolve().parents[3]
    module_path = repo_root / 'services' / service_name / 'main.py'
    spec = importlib.util.spec_from_file_location(f"{service_name}.main", str(module_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_social_service_root_endpoint():
    mod = load_main_module('social-service')
    app = mod.create_app()
    client = app.test_client()
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.get_json().get('status') == 'social-service ok'
