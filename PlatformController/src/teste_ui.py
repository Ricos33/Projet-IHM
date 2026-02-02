from textual.app import App, ComposeResult
from textual.widgets import Button
import ingescape as igs
import time

PORT = 5670

# ---- Déclaration de l’agent UI ----
igs.agent_set_name("TextualUI")
igs.definition_set_class("UI")
igs.definition_set_package("UI")

# ---- Choix du device réseau (le plus simple) ----
devices = igs.net_devices_list()
if len(devices) == 0:
    print("No network device found")
    exit(1)

device = devices[0]

# ---- Création de l’output (OBLIGATOIRE) ----
igs.output_create("User_Decision", igs.STRING_T, None)

# ---- Démarrage de l’agent UI ----
igs.start_with_device(device, PORT)


class TradingUI(App):

    def compose(self) -> ComposeResult:
        yield Button("BUY", id="buy")
        yield Button("SELL", id="sell")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "buy":
            igs.output_set_string("User_Decision", "BUY")
            self.log("BUY sent")

        elif event.button.id == "sell":
            igs.output_set_string("User_Decision", "SELL")
            self.log("SELL sent")


if __name__ == "__main__":
    TradingUI().run()
    igs.stop()
