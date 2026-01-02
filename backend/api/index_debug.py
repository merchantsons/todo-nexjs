# Debug version - test imports one by one
import sys
import traceback

print("Starting handler initialization...", flush=True)

try:
    print("Step 1: Importing FastAPI...", flush=True)
    from fastapi import FastAPI
    print("✅ FastAPI imported", flush=True)
except Exception as e:
    print(f"❌ FastAPI import failed: {e}", flush=True)
    traceback.print_exc(file=sys.stderr)
    raise

try:
    print("Step 2: Importing Mangum...", flush=True)
    from mangum import Mangum
    print("✅ Mangum imported", flush=True)
except Exception as e:
    print(f"❌ Mangum import failed: {e}", flush=True)
    traceback.print_exc(file=sys.stderr)
    raise

try:
    print("Step 3: Creating minimal app...", flush=True)
    app = FastAPI()
    print("✅ Minimal app created", flush=True)
except Exception as e:
    print(f"❌ App creation failed: {e}", flush=True)
    traceback.print_exc(file=sys.stderr)
    raise

try:
    print("Step 4: Creating Mangum handler...", flush=True)
    handler = Mangum(app, lifespan="off")
    print("✅ Handler created", flush=True)
except Exception as e:
    print(f"❌ Handler creation failed: {e}", flush=True)
    traceback.print_exc(file=sys.stderr)
    raise

print("✅✅✅ All initialization complete! ✅✅✅", flush=True)


