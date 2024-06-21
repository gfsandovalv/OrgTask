from textual.widgets import DataTable, Header, Label, Footer
from rich.text import Text
from pandas import DataFrame, Series
from textual.screen import Screen
from textual.app import ComposeResult
import sys
sys.path.append('../') 
from info import APP_NAME

class TaskExplorer(Screen):
    table = DataTable(cursor_type='row')
    TITLE = "Task Explorer"
    SUB_TITLE = APP_NAME
    
    def __init__(self, df, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.df = df

    def fill_table(self, df):
        table = self.query_one(DataTable)
        if type(df) == DataFrame:
            table.add_columns(*df.columns.tolist())
            table.add_rows(df.values.tolist())
        elif type(df) == Series:
            table.add_columns(*(df.name,))
            table.add_rows([[x] for x in df.values.tolist()])
 
    def compose(self) -> ComposeResult:
        yield Header()
        yield self.table
        yield Label("asd")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = 'row'
        self.fill_table(self.df)
    def on_data_table_row_highlighted(self, message: DataTable.RowHighlighted) -> None:
        a = self.table.get_row(message.row_key)
        self.query_one(Label).update(str(a))
    
