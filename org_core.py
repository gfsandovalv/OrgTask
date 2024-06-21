import orgparse
import re
from pandas import Series, DataFrame

def starts_with_number(s):
    pattern = re.compile(r'^\s*\d+\.\s*')
    return bool(pattern.match(s))

def get_lists(body):
    """if there's more than one list inside the body, those are concatenated
    """
    non_markable_list_chars = ('- ', '+ ', '- [x]', '- [-]')
    markable_list_chars = ('- [ ]', '- [x]', '- [-]')
    
    m_lists = [x for x in body if x.startswith(markable_list_chars)]
    nm_lists = [x for x in body if x.startswith(non_markable_list_chars)]
    num_lists = [x for x in body if starts_with_number(x)]
    
    return m_lists + nm_lists + num_lists

def object_attributes(obj):
    attr_dict = vars(obj)
    all_attrs = dir(obj)
    # Filtering out methods and built-in attributes to add to the dictionary
    additional_attrs = {attr: getattr(obj, attr) for attr in all_attrs if not callable(getattr(obj, attr)) and not attr.startswith('__')}
    attr_dict.update(additional_attrs)
    return attr_dict
        
class OrgAgenda():
    def __init__(self, file_path) -> None:
        self.root = orgparse.load(file_path)
        self.title = self.root.get_file_property('TITLE')
        self.author = self.root.get_file_property('AUTHOR')
        self.creation_date = self.root.get_file_property('DATE')
        self.tasks_raw =  self.root.children
        # tasks into a pandas series
        _task_list = [OrgTask(task_node) for task_node in self.root.children]
        self.tasks =  DataFrame(data=
                                {
                                    "Task name" : [x.heading for x in _task_list],
                                    "OrgTask_obj" : _task_list}, 
                             index = [x.heading for x in _task_list])

        
    def get_summaries(self):
        self.summaries = [task.get_summary() for task in self.tasks]
        return self.summaries

class OrgTask():
    def __init__(self, node) -> None:
        self._lines = node._lines
        self.heading = node.heading if node.heading else None

        # time and dates
        self.has_date = node.has_date() if node.has_date() else None
        self.scheduled = node.scheduled if node.scheduled else None
        self.deadline = node.deadline if node.deadline else None
        self.closed = node.closed if node.closed else None
        self.datelist = node.datelist if node.datelist else None
        self.clock = node.clock if node.clock else None

        self.properties = node.properties if node.properties else None
        self.tags = node.tags if node.tags else None
        self.body = node.body if node.body else None
        self.lists = get_lists(self.body.split('\n')) if self.body else None
        self.priority = node.priority if node.priority else None

    def get_summary(self):
        self.summary_dict = None
        summary_dict = object_attributes(self)
        summary_dict.pop('_lines')
        summary_dict.pop('summary_dict')
        return summary_dict
        
