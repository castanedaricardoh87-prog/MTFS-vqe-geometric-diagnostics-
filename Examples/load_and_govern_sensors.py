# examples/load_and_govern_sensors.py
"""
Minimal sensor → governor example for MTFS / VQE diagnostics.

Shows the recommended contract:
  raw sensors → frozen calibration ranges → [0, 18] channels → governor → M'
"""

from sensor_loaders import load_csv_sensors

# 1. Point at any lab CSV (or use the demo)
data = load_csv_sensors(
    "demo_lab_sensors.csv",          # or your real log
    column_map={"p": "temp_C", "e": "hall_mV", "s": "refl_dBm"},
    time_column="time_s",
    # 2. Freeze the ranges once per campaign (critical for comparability)
    ranges={
        "p": (23.0, 36.0),
        "e": (8.0, 40.0),
        "s": (-22.0, -5.0),
    },
    out_max_per_channel=18.0,
    apply_gov=True,                  # hard-caps M' ≤ 31
    keep_raw=True,                   # keeps original values for audit
)

print(f"Samples loaded : {len(data['m_p'])}")
print(f"Max M'         : {data['M_prime'].max():.1f}")
print(f"M' always ≤ 31 : {bool(data['M_prime'].max() <= 31.0)}")
