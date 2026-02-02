#!/usr/bin/env python3
# coding: utf-8

import ingescape as igs
import time
import json

# --- Nom de l'agent ---
igs.agent_set_name("AssetManager_Simple")

# --- Définition ---
igs.definition_set_class("AssetManager_Simple")
igs.definition_set_package("Agents")

# --- Output DATA ---
igs.output_create("Available_Assets", igs.DATA_T, None)

# --- Choix du device ---
devices = igs.net_devices_list()
if not devices:
    print("No network device found")
    exit(1)

device = devices[0]
PORT = 5670

# --- Démarrage ---
igs.start_with_device(device, PORT)
print("[AssetManager] Agent started")

# --- Donnée EXISTANTE (STRUCTURÉE) ---
assets = {
    "stocks": ["AAPL", "TSLA", "AMZN"],
    "crypto": ["BTC", "ETH"],
    "forex": ["EURUSD"]
}

# --- Conversion en DATA ---
assets_bytes = json.dumps(assets).encode("utf-8")

time.sleep(1)
igs.output_set_data("Available_Assets", assets_bytes)

print("[AssetManager] Available_Assets sent (DATA)")

# --- Boucle ---
try:
    while igs.is_started():
        time.sleep(1)
except KeyboardInterrupt:
    pass

igs.stop()
print("[AssetManager] Agent stopped")
