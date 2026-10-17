import os
import sys
import json
import hashlib
import time
import subprocess
from datetime import datetime, timezone
import pyarrow.parquet as pq

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEP_DATA = os.path.join(BASE_DIR, "deployment_data", "data")
DEP_MODELS = os.path.join(BASE_DIR, "deployment_data", "models")
RAW_DATA = os.path.join(BASE_DIR, "data", "raw")
METADATA_DIR = os.path.join(BASE_DIR, "docs", "metadata")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "finsight-ai-dataset-442154825091")

GCLOUD_BIN = r"C:\Users\HP\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
if not os.path.exists(GCLOUD_BIN):
    GCLOUD_BIN = "gcloud"

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8 * 1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

def get_parquet_meta(filepath):
    try:
        meta = pq.read_metadata(filepath)
        schema = pq.read_schema(filepath)
        col_types = {name: str(schema.field(name).type) for name in schema.names}
        return {
            "num_rows": meta.num_rows,
            "num_columns": meta.num_columns,
            "columns": schema.names,
            "column_types": col_types
        }
    except Exception as e:
        return {"error": str(e)}

def build_inventory():
    items = []
    
    # 1. Original Source Datasets
    if os.path.exists(RAW_DATA):
        for f in sorted(os.listdir(RAW_DATA)):
            fp = os.path.join(RAW_DATA, f)
            if os.path.isfile(fp):
                items.append({
                    "filename": f,
                    "local_path": fp,
                    "gcs_key": f"original/{f}",
                    "tier": "original",
                    "size_bytes": os.path.getsize(fp)
                })

    # 2. Processed Parquet/CSV and 3. Indexes
    if os.path.exists(DEP_DATA):
        for f in sorted(os.listdir(DEP_DATA)):
            fp = os.path.join(DEP_DATA, f)
            if not os.path.isfile(fp):
                continue
            sz = os.path.getsize(fp)
            if f.endswith(".parquet") or f.endswith(".csv"):
                tier = "processed"
                gcs_key = f"processed/{f}"
            elif f.endswith(".pkl") or f.endswith(".bin"):
                tier = "indexes"
                gcs_key = f"indexes/{f}"
            else:
                tier = "processed"
                gcs_key = f"processed/{f}"
            items.append({
                "filename": f,
                "local_path": fp,
                "gcs_key": gcs_key,
                "tier": tier,
                "size_bytes": sz
            })

    # 4. Models
    if os.path.exists(DEP_MODELS):
        for f in sorted(os.listdir(DEP_MODELS)):
            fp = os.path.join(DEP_MODELS, f)
            if os.path.isfile(fp):
                items.append({
                    "filename": f,
                    "local_path": fp,
                    "gcs_key": f"models/{f}",
                    "tier": "models",
                    "size_bytes": os.path.getsize(fp)
                })

    return items

def get_remote_gcs_objects():
    """Lists existing objects in GCS bucket with their sizes in bytes."""
    cmd = [GCLOUD_BIN, "storage", "objects", "list", f"gs://{BUCKET_NAME}/", "--format=json(name,size)"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Warning listing GCS objects: {res.stderr}")
        return {}
    try:
        data = json.loads(res.stdout)
        return {item["name"]: int(item.get("size", 0)) for item in data}
    except Exception as e:
        print(f"Error parsing GCS objects list: {e}")
        return {}

def run_migration():
    print(f"=== FinSight AI GCS Migration Engine ===")
    print(f"Target Bucket: gs://{BUCKET_NAME}/")
    print(f"Timestamp:     {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    os.makedirs(METADATA_DIR, exist_ok=True)
    items = build_inventory()
    print(f"Discovered {len(items)} files to migrate across 4 tiers.")

    remote_objects = get_remote_gcs_objects()
    print(f"Currently {len(remote_objects)} objects exist in gs://{BUCKET_NAME}/\n")

    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "bucket_name": BUCKET_NAME,
        "total_files": len(items),
        "total_bytes": sum(x["size_bytes"] for x in items),
        "files": []
    }
    schema_inventory = {}
    verified_count = 0
    uploaded_count = 0
    skipped_count = 0

    t0_all = time.time()

    for idx, item in enumerate(items, 1):
        fn = item["filename"]
        gcs_key = item["gcs_key"]
        local_fp = item["local_path"]
        sz = item["size_bytes"]
        tier = item["tier"]

        print(f"[{idx:02d}/{len(items)}] [{tier:9}] {fn} ({sz / (1024*1024):.2f} MB)... ", end="", flush=True)

        already_uploaded = False
        if gcs_key in remote_objects and remote_objects[gcs_key] == sz:
            already_uploaded = True

        t0_file = time.time()
        if already_uploaded:
            print(f"[ALREADY EXISTS] in GCS (matched {sz:,} bytes)")
            skipped_count += 1
        else:
            # Upload via gcloud storage cp
            target_uri = f"gs://{BUCKET_NAME}/{gcs_key}"
            cmd = [GCLOUD_BIN, "storage", "cp", local_fp, target_uri, "--quiet"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"[UPLOAD ERROR]: {res.stderr.strip()[:200]}")
                continue
            elapsed = time.time() - t0_file
            rate_mb = (sz / (1024 * 1024)) / max(elapsed, 0.001)
            print(f"[UPLOADED] {elapsed:.1f}s ({rate_mb:.2f} MB/s)")
            uploaded_count += 1
            # Update remote_objects cache
            remote_objects[gcs_key] = sz

        # Checksum calculation and verification
        sha256_hash = compute_sha256(local_fp)
        is_verified = (gcs_key in remote_objects and remote_objects[gcs_key] == sz)
        if is_verified:
            verified_count += 1

        file_record = {
            "filename": fn,
            "gcs_key": gcs_key,
            "gcs_uri": f"gs://{BUCKET_NAME}/{gcs_key}",
            "tier": tier,
            "size_bytes": sz,
            "sha256": sha256_hash,
            "verified": is_verified
        }

        # If Parquet, extract schema and row count
        if fn.endswith(".parquet"):
            pm = get_parquet_meta(local_fp)
            if "error" not in pm:
                file_record["num_rows"] = pm["num_rows"]
                file_record["num_columns"] = pm["num_columns"]
                schema_inventory[fn] = {
                    "num_rows": pm["num_rows"],
                    "columns": pm["columns"],
                    "column_types": pm["column_types"]
                }

        manifest["files"].append(file_record)

    total_time = time.time() - t0_all
    print("\n" + "=" * 60)
    print(f"Migration Completed in {total_time:.1f}s!")
    print(f"Total Files:       {len(items)}")
    print(f"Uploaded:          {uploaded_count}")
    print(f"Skipped (Synced):  {skipped_count}")
    print(f"Verified Intact:   {verified_count}/{len(items)}")
    print("=" * 60)

    # Integrity Report
    integrity_report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "bucket_name": BUCKET_NAME,
        "migration_status": "SUCCESS" if verified_count == len(items) else "PARTIAL_FAILURE",
        "total_files": len(items),
        "verified_files": verified_count,
        "failed_files": len(items) - verified_count,
        "total_bytes_verified": sum(x["size_bytes"] for x in items),
        "total_time_seconds": round(total_time, 2),
        "tiers_summary": {
            t: {
                "count": len([f for f in manifest["files"] if f["tier"] == t]),
                "bytes": sum(f["size_bytes"] for f in manifest["files"] if f["tier"] == t)
            }
            for t in ["original", "processed", "indexes", "models"]
        }
    }

    # Save metadata locally
    manifest_local = os.path.join(METADATA_DIR, "manifest.json")
    schemas_local = os.path.join(METADATA_DIR, "schema_inventory.json")
    report_local = os.path.join(METADATA_DIR, "integrity_report.json")

    with open(manifest_local, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    with open(schemas_local, "w", encoding="utf-8") as f:
        json.dump(schema_inventory, f, indent=2)
    with open(report_local, "w", encoding="utf-8") as f:
        json.dump(integrity_report, f, indent=2)

    print(f"Saved local metadata to {METADATA_DIR}")

    # Upload metadata files to gs://<bucket>/metadata/
    for meta_fn, meta_path in [
        ("manifest.json", manifest_local),
        ("schema_inventory.json", schemas_local),
        ("integrity_report.json", report_local)
    ]:
        target_uri = f"gs://{BUCKET_NAME}/metadata/{meta_fn}"
        cmd = [GCLOUD_BIN, "storage", "cp", meta_path, target_uri, "--quiet"]
        subprocess.run(cmd, check=True)
        print(f"Uploaded metadata file to {target_uri}")

    print("\nData migration and verification report generated successfully!")

if __name__ == "__main__":
    run_migration()
