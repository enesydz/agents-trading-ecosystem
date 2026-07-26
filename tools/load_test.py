"""Small standard-library latency smoke test for a running API."""

import argparse
import statistics
import time
import urllib.request


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000/health")
    parser.add_argument("--requests", type=int, default=20)
    args = parser.parse_args()
    durations = []
    for _ in range(args.requests):
        started = time.perf_counter()
        with urllib.request.urlopen(args.url, timeout=5) as response:
            response.read()
        durations.append(time.perf_counter() - started)
    print(
        f"requests={len(durations)} p50={statistics.median(durations):.4f}s "
        f"max={max(durations):.4f}s"
    )


if __name__ == "__main__":
    main()
