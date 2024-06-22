from textual.widgets import DataTable, Header, Label, Footer, Static, Markdown
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
    
    def __init__(self, agenda, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.task_list = agenda.tasks['Task name']
        self.agenda_summaries = agenda.tasks['summaries']

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
        
        yield Markdown()
        yield Label()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = 'row'
        self.fill_table(self.task_list)

    def on_data_table_row_highlighted(self, message: DataTable.RowHighlighted) -> None:
        row = self.table.get_row(message.row_key)
        self.query(Markdown)[0].update(self.agenda_summaries[row[0]])
    
        