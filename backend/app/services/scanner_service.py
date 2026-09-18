import importlib.util
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _load_scanner_module() -> Any:
    scanner_path = Path(__file__).parents[3] / "aws-security" / "scanner.py"
    if not scanner_path.exists():
        raise RuntimeError("AWS scanner is not available in this checkout")
    spec = importlib.util.spec_from_file_location("cloudshield_aws_scanner", scanner_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load AWS scanner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scan_aws() -> dict[str, list[dict[str, Any]]]:
    """Invoke the existing scanner and normalize its two result collections."""
    module = _load_scanner_module()
    scanner = getattr(module, "scan", None) or getattr(module, "run_scan", None)
    if scanner is None:
        raise RuntimeError("AWS scanner does not expose scan or run_scan")
    result = scanner()
    if not isinstance(result, dict):
        raise RuntimeError("AWS scanner returned an invalid result")
    return {
        "resources": list(result.get("resources", [])),
        "findings": list(result.get("findings", [])),
    }
