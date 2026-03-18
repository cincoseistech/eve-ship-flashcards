import subprocess
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))

def ensure_data():
    sde_path = os.path.join(APP_DIR, "sde.sqlite")
    xlsx_path = os.path.join(APP_DIR, "eve_ships_complete.xlsx")

    if not os.path.exists(sde_path):
        print("Downloading SDE...")
        subprocess.run([
            "curl", "-L", "-o", sde_path + ".bz2",
            "https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2"
        ], check=True)
        print("Decompressing...")
        import bz2
        import shutil
        with bz2.BZ2File(sde_path + ".bz2") as fr, open(sde_path, "wb") as fw:
            shutil.copyfileobj(fr, fw)
        os.remove(sde_path + ".bz2")

    if not os.path.exists(xlsx_path):
        print("Exporting ship data...")
        subprocess.run(["python", os.path.join(APP_DIR, "export_ships.py")], check=True)

if __name__ != "__main__":
    ensure_data()
