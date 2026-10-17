import os
import json
import hashlib
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEP_DATA = os.path.join(BASE_DIR, "deployment_data", "data")
DEP_MODELS = os.path.join(BASE_DIR, "deployment_data", "models")
RAW_DATA = os.path.join(BASE_DIR, "data", "raw")
BUCKET_NAME = "finsight-ai-dataset-442154825091"

def plan_migration():
    items = []
    
    # 1. Original Source Datasets
    if os.path.exists(RAW_DATA):
        for f in os.listdir(RAW_DATA):
            fp = os.path.join(RAW_DATA, f)
            if os.path.isfile(fp):
                items.append({
                    "filename": f,
                    "local_path": fp,
                    "gcs_key": f"original/{f}",
                    "tier": "original",
                    "size_bytes": os.path.getsize(fp)
                })

    # 2. Processed Parquet/CSV and 3. Indexes/Lookups
    if os.path.exists(DEP_DATA):
        for f in os.listdir(DEP_DATA):
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
        for f in os.listdir(DEP_MODELS):
            fp = os.path.join(DEP_MODELS, f)
            if os.path.isfile(fp):
                items.append({
                    "filename": f,
                    "local_path": fp,
                    "gcs_key": f"models/{f}",
                    "tier": "models",
                    "size_bytes": os.path.getsize(fp)
                })

    total_bytes = sum(x["size_bytes"] for x in items)
    print(f"Total planned migration files: {len(items)}")
    print(f"Total planned migration size:  {total_bytes / (1024**3):.3f} GB ({total_bytes:,} bytes)")
    
    by_tier = {}
    for x in items:
        by_tier.setdefault(x["tier"], []).append(x)
        
    for t, file_list in sorted(by_tier.items()):
        t_bytes = sum(f["size_bytes"] for f in file_list)
        print(f"  Tier '{t:10}': {len(file_list):2} files | {t_bytes / (1024**3):.3f} GB ({t_bytes:,} bytes)")

    return items

if __name__ == "__main__":
    plan_migration()
