from textual.app import App, ComposeResult
from info import APP_NAME, VERSION
from org_sight.screens import TaskExplorer
import org_core
agenda = org_core.OrgAgenda('example_orgs/example0.org')


class MainApp(App):
    BINDINGS = [
        ("l", "switch_mode('full_list')", "Detailed list"),  
    ]
    MODES = {
        "full_list": TaskExplorer(agenda),  
    }

    def on_mount(self) -> None:
        self.switch_mode("full_list")  


app = MainApp()
if __name__ == "__main__":
    app.run()