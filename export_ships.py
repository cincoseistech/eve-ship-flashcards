import sqlite3
import pandas as pd
import sys
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sde.sqlite")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eve_ships_complete.xlsx")


def export():
    if not os.path.exists(DB_PATH):
        print(f"ERROR: SDE database not found at {DB_PATH}")
        print("Run the launcher script to download it automatically.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)

    print("Querying ships...")
    ships_query = """
    SELECT t.typeID, t.typeName, g.groupName, t.mass, t.volume, t.capacity,
           mg.marketGroupName
    FROM invTypes t
    JOIN invGroups g ON t.groupID = g.groupID
    JOIN invCategories c ON g.categoryID = c.categoryID
    LEFT JOIN invMarketGroups mg ON t.marketGroupID = mg.marketGroupID
    WHERE c.categoryID = 6 AND t.published = 1
    """
    ships_df = pd.read_sql_query(ships_query, conn)
    print(f"  Found {len(ships_df)} ships")

    print("Querying attributes...")
    attr_query = """
    SELECT ta.typeID,
           da.attributeName,
           COALESCE(ta.valueFloat, ta.valueInt) AS value
    FROM dgmTypeAttributes ta
    JOIN dgmAttributeTypes da ON ta.attributeID = da.attributeID
    WHERE ta.typeID IN (
        SELECT t.typeID FROM invTypes t
        JOIN invGroups g ON t.groupID = g.groupID
        JOIN invCategories c ON g.categoryID = c.categoryID
        WHERE c.categoryID = 6 AND t.published = 1
    )
    """
    attrs_df = pd.read_sql_query(attr_query, conn)
    print(f"  Found {len(attrs_df)} attribute entries")

    print("Pivoting attributes...")
    attrs_pivot = attrs_df.pivot_table(
        index='typeID',
        columns='attributeName',
        values='value',
        aggfunc='first'
    ).reset_index()

    result = ships_df.merge(attrs_pivot, on='typeID', how='left')

    priority_cols = [
        'typeID', 'typeName', 'groupName', 'marketGroupName',
        'mass', 'volume', 'capacity',
    ]
    existing_priority = [c for c in priority_cols if c in result.columns]
    remaining = [c for c in result.columns if c not in existing_priority]
    result = result[existing_priority + remaining]

    print(f"Writing {OUTPUT_PATH}...")
    result.to_excel(OUTPUT_PATH, index=False)
    print(f"Done. {len(result)} ships, {len(result.columns)} columns.")

    conn.close()


if __name__ == "__main__":
    export()
