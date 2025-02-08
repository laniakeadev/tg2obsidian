import json
import os
from datetime import datetime

SCRIPT_VERSION = "8.2.25-1"
METADATA_FILE = ".tg2obsidian_metadata.json" 

def write_metadata(path):
    metadata = {
    "version": SCRIPT_VERSION,
    "timestamp": datetime.now().isoformat()
    }
    
    file = os.path.join(path, METADATA_FILE)
    os.system( "attrib -h {f}".format(f = file) )
    with open(file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    os.system( "attrib +h {f}".format(f = file) )


def read_metadata(path):
    file = os.path.join(path, METADATA_FILE)
    os.system( "attrib -h {f}".format(f = file) )
    if not os.path.exists(file):
        return None
    
    with open(file, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    
    os.system( "attrib +h {f}".format(f = file) )
    return metadata

def check(path):
    metadata = read_metadata(path)
    if metadata is not None:
        print(f"Previous export found: {metadata["timestamp"]}")
    else:
        print("Metadata is none")