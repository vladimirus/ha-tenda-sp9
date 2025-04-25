# Tenda SP9 / SP3 Smart Plug with Energy Monitoring – Home Assistant integration

Control and monitor Tenda SP9 smart plugs — and likely SP3 units as well (energy sensor may be missing) — locally from Home Assistant, with no Tenda cloud or mobile app required.

---

## Features

- Toggle the plug on/off
- Live power (`W`) and accumulated energy (`kWh`) sensors
- Local pairing helper script (Linux/macOS/Windows)

---

## 1  Install through HACS

1. **HACS → Settings → Custom repositories**  
   Add
   ```
   https://github.com/vladimirus/ha-tenda-sp9
   ```  
   Category = **Integration**.
2. **HACS → Integrations → Explore & Download**  
   Search **Tenda Beli Plug** → **Download** → **Restart Home Assistant**.

*(Manual install: copy `custom_components/tendabeli` into `config/custom_components/`, restart HA.)*

---

## 2  Pair a new SP9 socket

> The **last four digits of the socket’s S/N** become its entity identifier (example `0578`).

### 2-1  Put the plug in pairing mode
1. Hold the button until the LED blinks **red / blue**.
2. The plug now exposes a Wi-Fi hotspot (e.g. `SP9_0578`).

### 2-2  Send Wi-Fi and HA details
1. Connect your laptop to the hotspot.
2. In this repo:
   ```bash
   cd pair_socket
   ```
3. Edit **`config.txt`** with **your** Wi-Fi SSID, password and Home-Assistant IP/hostname:

   ```json
   {"account":"1",
    "ssid":"YOUR_WIFI_NAME",
    "key":"YOUR_WIFI_PASSWORD",
    "server":"YOUR_HA_IP",
    "location":"Europe/London",
    "time_zone":0}
   ```

4. Run the helper:

   **Linux / macOS**

   ```bash
   ./run.sh
   ```

   **Windows**

   ```powershell
   # PowerShell
   .\run.ps1
   ```
   or double‑click **run.bat**

   After a few seconds the plug “clicks” and joins your home network.

---

## 3  Entities created

| Entity | Example ID | Purpose |
|--------|------------|---------|
| **Switch** | `switch.tbp_switch_0578` | Turn the plug on/off |
| **Power sensor** | `sensor.tbp_power_0578` | Instantaneous power (W) |
| **Energy sensor** | `sensor.tbp_energy_0578` | Lifetime energy (kWh) |

Find them in **Settings → Entities** (search `tbp*`).

---

## 4  Optional: friendly names

Add to `configuration.yaml` or `customize.yaml`:

```yaml
switch.tbp_switch_0578:
  friendly_name: "Fridge Plug Switch"
sensor.tbp_power_0578:
  friendly_name: "Fridge Plug Power"
sensor.tbp_energy_0578:
  friendly_name: "Fridge Plug Energy"
```

Save → *Developer Tools → YAML → Reload Location & Customizations*.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| No `tbp_*` entities appear | Ensure plug and HA are on same LAN; re-run `./run.sh` and wait 60 s. |
| Want to re-pair | Long-press the plug button again and repeat **Pair** steps. |

PRs and issues welcome!
