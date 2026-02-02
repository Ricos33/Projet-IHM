from textual.app import App, ComposeResult
from textual.widgets import Select, Static
import ingescape as igs
import json

# ===============================
# INGESCAPE INIT
# ===============================

PORT = 5670

igs.agent_set_name("TextualUI")
igs.definition_set_class("UI")
igs.definition_set_package("UI")

devices = igs.net_devices_list()
if not devices:
    print("No network device found")
    exit(1)

device = devices[0]

igs.input_create("Available_Assets", igs.DATA_T, None)
igs.output_create("Asset_ID", igs.STRING_T, None)

igs.start_with_device(device, PORT)

# ===============================
# GLOBAL DATA
# ===============================

ASSETS = {}
ASSETS_LOADED = False

# ===============================
# INGESCAPE CALLBACK
# ===============================

def Available_Assets_input_callback(io_type, name, value_type, value, my_data):
    global ASSETS, ASSETS_LOADED
    ASSETS = json.loads(value.decode("utf-8"))
    ASSETS_LOADED = True
    print("[TextualUI] Assets received")

igs.observe_input("Available_Assets", Available_Assets_input_callback, None)

# ===============================
# TEXTUAL APP
# ===============================

class TradingUI(App):

    def compose(self) -> ComposeResult:
        yield Static("Select an asset to work on")
        yield Select([], id="asset_select")

    def on_mount(self):
        # 🔁 vérifier régulièrement si les assets sont arrivés
        self.set_interval(0.5, self.check_assets)

    def check_assets(self):
        global ASSETS_LOADED

        if not ASSETS_LOADED:
            return

        select = self.query_one("#asset_select", Select)

        # éviter rechargement multiple
        if select.options:
            return

        options = []
        for category, assets in ASSETS.items():
            for asset in assets:
                options.append((f"{category} - {asset}", asset))

        select.options = options
        self.log("Assets loaded into Select")

    def on_select_changed(self, event: Select.Changed):
        igs.output_set_string("Asset_ID", event.value)
        self.log(f"Asset selected: {event.value}")

# ===============================
# MAIN
# ===============================

if __name__ == "__main__":
    try:
        TradingUI().run()
    finally:
        igs.stop()
