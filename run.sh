#!/bin/bash
cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 -c "
import asyncio
import sys
from server import server

async def main():
    await server.run(sys.stdin.buffer, sys.stdout.buffer)

asyncio.run(main())
"
