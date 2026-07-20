#!python3
# https://download.geonames.org/export/dump/readme.txt

from pathlib import Path
import io
import sqlite3
import urllib.request
import zipfile

DATASET = "cities15000"
URL = "https://download.geonames.org/export/dump"
DATABASE = Path("geonames.db")
HEADER = Path("src") / Path("geonames.db.h")

def get_file(filename, key, name):
    url = f"{URL}/{filename}"
    print(f"Downloading {url}")
    lookup = {}
    text = urllib.request.urlopen(url).read().decode("utf-8")
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        lookup[fields[key]] = fields[name]
    return lookup

def get_rows():
    admin1 = get_file("admin1CodesASCII.txt", 0, 1)
    admin2 = get_file("admin2Codes.txt", 0, 2)
    countries = get_file("countryInfo.txt", 0, 4)
    url = f"{URL}/{DATASET}.zip"
    print(f"Downloading {url}")
    data = urllib.request.urlopen(url).read()
    archive = zipfile.ZipFile(io.BytesIO(data))
    with archive.open(f"{DATASET}.txt") as raw:
        for line in io.TextIOWrapper(raw, encoding="utf-8"):
            fields = line.rstrip("\n").split("\t")
            name = fields[2]
            latitude = float(fields[4])
            longitude = float(fields[5])
            country = fields[8]
            admin1_code = fields[10]
            admin2_code = fields[11]
            population = int(fields[14] or 0)
            parts = [name]
            county = admin2.get(f"{country}.{admin1_code}.{admin2_code}")
            state = admin1.get(f"{country}.{admin1_code}")
            nation = countries.get(country, country)
            if county:
                parts.append(county)
            if state:
                parts.append(state)
            if nation:
                parts.append(nation)
            location = ", ".join(parts)
            yield (location, latitude, longitude, population)

def main():
    if DATABASE.exists():
        DATABASE.unlink()
    database = sqlite3.connect(DATABASE)
    database.execute(
        "CREATE VIRTUAL TABLE cities USING fts5("
        "location, latitude UNINDEXED, longitude UNINDEXED, population UNINDEXED)"
    )
    rows = database.executemany(
        "INSERT INTO cities(location, latitude, longitude, population) VALUES (?, ?, ?, ?)",
        get_rows(),
    ).rowcount
    database.commit()
    database.close()
    data = DATABASE.read_bytes()
    with open(HEADER, "w") as header:
        header.write("#pragma once\n\n")
        header.write("static unsigned char kGeoNames[] = \n{\n")
        for offset in range(0, len(data), 20):
            header.write("".join(f"0x{byte:02x}," for byte in data[offset:offset + 20]) + "\n")
        header.write("};\n")
    print(f"Wrote {rows} cities to {HEADER} ({DATABASE.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
