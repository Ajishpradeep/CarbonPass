"""CarbonPass command-line interface.

Commands (filled in as the pipeline lands):
    carbonpass ingest <firm_dir> -o out.json     # docs -> activity data JSON
    carbonpass pack <activity.json> -o out.xlsx  # activity data -> filled Communication Template
    carbonpass costdelta <activity.json>         # default-vs-actual buyer screen
"""
from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="carbonpass", description=__doc__)
    sub = parser.add_subparsers(dest="command")

    p_ingest = sub.add_parser("ingest", help="Parse a firm's document folder into activity-data JSON")
    p_ingest.add_argument("firm_dir")
    p_ingest.add_argument("-o", "--output", default=None)
    p_ingest.add_argument("--no-vlm", action="store_true", help="structured parsers only (no Ollama)")

    p_pack = sub.add_parser("pack", help="Activity JSON -> filled CBAM Communication Template .xlsx")
    p_pack.add_argument("activity_json")
    p_pack.add_argument("-o", "--output", default=None)

    p_cost = sub.add_parser("costdelta", help="Default-vs-actual buyer cost screen")
    p_cost.add_argument("activity_json")

    p_sched = sub.add_parser("schedule", help="Module 2: grid-aware TOU shift plan + ledger")
    p_sched.add_argument("firm_dir")
    p_sched.add_argument("-o", "--output", default=None)
    p_sched.add_argument("--month", type=int, default=7, help="tariff month (season)")

    p_serve = sub.add_parser("serve", help="Module 3: FastAPI server (incl. LINE webhook)")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8787)

    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 1

    if args.command == "ingest":
        from carbonpass.ingestion.pipeline import run_ingest_cli

        return run_ingest_cli(args.firm_dir, args.output, use_vlm=not args.no_vlm)
    if args.command == "pack":
        from carbonpass.writer.fill import run_pack_cli

        return run_pack_cli(args.activity_json, args.output)
    if args.command == "costdelta":
        from carbonpass.costdelta.screen import run_costdelta_cli

        return run_costdelta_cli(args.activity_json)
    if args.command == "schedule":
        from carbonpass.scheduler.ledger import run_schedule_cli

        return run_schedule_cli(args.firm_dir, args.output, month=args.month)
    if args.command == "serve":
        import uvicorn

        from carbonpass.api.app import app

        uvicorn.run(app, host=args.host, port=args.port)
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
