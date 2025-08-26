from pathlib import Path


def parse_truedata_docs(doc_path: Path | None = None):
    if doc_path is None:
        doc_path = Path(__file__).resolve().parents[1] / "docs/truedata_sdk.md"
    endpoints = []
    with open(doc_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("|") and not line.startswith("| Endpoint") and not line.startswith("|-"):
                parts = [p.strip() for p in line.strip().split("|")[1:-1]]
                if len(parts) >= 6:
                    endpoint, method, req, resp, rate, notes = parts[:6]
                    endpoints.append({
                        "provider": "TrueData",
                        "endpoint_url": endpoint,
                        "method": method,
                        "request_schema": req,
                        "response_schema": resp,
                        "rate_limit": rate,
                        "notes": notes,
                    })
    return endpoints


if __name__ == "__main__":
    import json

    print(json.dumps(parse_truedata_docs(), indent=2))
