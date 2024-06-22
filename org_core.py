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

def _date_str(date, keyword=''):
    date_attrs = date.__dict__
    summary_lines = ''

    start = date_attrs['_start'] if date_attrs['_start'] else ''
    end = date_attrs['_end'] if date_attrs['_end'] else ''

    if start and not end:
        summary_lines += keyword.capitalize() + ' for ' + start.strftime("%B %d, %Y")

    elif end and not start:
        summary_lines += keyword.capitalize() + ' ending in ' + end.strftime("%B %d, %Y")
    
    elif start and end:
        summary_lines += keyword.capitalize() + ' starting in ' + start.strftime("%B %d, %Y") + ', and is ending in ' + end.strftime("%B %d, %Y")

    return summary_lines    

def markdow_summary(task, string=False):
    t = task
    summary_lines = ['# ' + t.heading]

    scheduled = _date_str(task.scheduled, 'scheduled')
    deadline = _date_str(task.deadline, 'deadline')
    

    if bool(scheduled):
        summary_lines.append(scheduled)

    if bool(deadline):
        summary_lines.append(deadline)
    
    if bool(task.clock):
        clock = _date_str(task.clock[0], 'clock')
        summary_lines.append(clock)

    summary_lines.append(t.body)
    
    # TODO añadir más detalles de las tareas children, ya se tiene el máximo nivel de profundidad, así que se puede iterar fácilmente
    # children summary, at the momment just headings
    if t.children:
        for x in t.children:
            summary_lines.append('## ' + x.heading)
    
    if string:
        return '\n'.join(summary_lines)
    else:
        return summary_lines

def get_max_level(base_node):
    max_level = 0

    def traverse(node):
        nonlocal max_level
        if node.level > max_level:
            max_level = node.level
        for child in node.children:
            traverse(child)
    
    traverse(base_node)
    return max_level


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

        self.tasks['summaries'] = [task.string_summary for task in self.tasks['OrgTask_obj']]
        self.nodes_max_level = [x.max_level for x in _task_list]
        self.max_level = max(self.nodes_max_level)


class OrgTask(org_parse.node.OrgNode):
    def __init__(self, src_obj=None, env=None, *args, **kwds) -> None:
        super().__init__(env=env, *args, **kwds)
        if src_obj:
            self.duplicate_attributes(src_obj)
        # TODO create summary in markdown format
        # TODO show children also in markdown format
        self.lists = get_lists(self.body.split('\n')) if self.body else None
        self.max_level = get_max_level(src_obj)
        self.string_summary = markdow_summary(src_obj, string=True)

    def duplicate_attributes(self, src_obj):
        for key, value in src_obj.__dict__.items():
            setattr(self, key, value)        


