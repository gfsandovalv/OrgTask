import org_parse
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
        self.root = org_parse.load(file_path)
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

        #self.tasks['summaries'] = [task.str_summary for task in self.tasks['OrgTask_obj']]

class OrgTask(org_parse.node.OrgNode):
    def __init__(self, src_obj=None, env=None, *args, **kwds) -> None:
        super().__init__(env=env, *args, **kwds)
        if src_obj:
            self.duplicate_attributes(src_obj)
        
        self.lists = get_lists(self.body.split('\n')) if self.body else None
        """self_attrs = self.__dict__
        keys = list(self_attrs.keys())
        to_remove = ('_lines', 'has_date')
        for r in to_remove:
            keys.remove(r)
        self.str_summary = '\n'.join([x + ' ' + str(self_attrs[x]) for x in keys])"""

    def duplicate_attributes(self, src_obj):
        for key, value in src_obj.__dict__.items():
            setattr(self, key, value)        

