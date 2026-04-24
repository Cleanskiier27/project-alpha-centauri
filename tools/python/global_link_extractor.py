"""
Global Thumbnail Link Extractor
Lists all direct URLs for the generated network thumbnails.
"""

import os
import json
from pathlib import Path

def extract_global_links(base_url="http://localhost:3000/network_thumbnails"):
    """Extracts and formats all thumbnail links"""
    thumb_dir = Path('network_thumbnails')
    metadata_path = thumb_dir / 'thumbnails.json'
    
    if not metadata_path.exists():
        print("❌ Metadata not found. Run extract_thumbnails.py first.")
        return []

    with open(metadata_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"🔗 GLOBAL_LINK_REPORT // {data['generated']}")
    print("="*80)
    
    links = []
    for device_id, info in data['devices'].items():
        link = f"{base_url}/{device_id}.html"
        links.append({
            "name": info['name'],
            "url": link,
            "status": info['status']
        })
        print(f"[{info['icon']}] {info['name']:<25} | {link}")

    print("="*80)
    print(f"✅ Extracted {len(links)} links.")
    return links

if __name__ == "__main__":
    extract_global_links()
