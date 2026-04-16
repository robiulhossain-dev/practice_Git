from django import forms
from tasks.models import Task, TaskDetail
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label="Task Description")
    due_date = forms.DateField(widget = forms.SelectDateWidget)
    assigned_to = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple, choices = [], label = "Assigned To")

    def __init__(self, *args, **kwargs):
        # print(args, kwargs)
        employees = kwargs.pop("employees",[])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]
        




    BIRTH_YEAR_CHOICES = ["1980", "1981", "1982"]
    BIRTH_MONTHS_CHOICES = {
    1: "January",
    2: "February",
    3: "November",
    }

    birth_year = forms.DateField(
        widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES, months=BIRTH_MONTHS_CHOICES)
    )

    FAVORITE_COLORS_CHOICES = {
    "1": "Blue",
    "2": "Green",
    "3": "Black",
    "4": "Orange"
    }

    favorite_colors = forms.ChoiceField(widget=forms.RadioSelect
    , choices=FAVORITE_COLORS_CHOICES, initial="4", label="My Favourite Color")

    CHOICES = {"1": "First", "2": "Second", "3": "Third"}
    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, initial="2")



class StyledForMixin():
    """Mixin to apply style to form field"""
    default_classes = "border-2  border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
    def apply_styled_widget(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder' : f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class' : f"{self.default_classes}",
                    'style': 'resize: none;',
                    'placeholder' : f"Enter {field.label.lower()}",
                    'rows' : 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : "border-2 border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : "space-y-2"
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': self.default_classes.replace('w-full', 'w-48')
                    # 'style': 'resize: none;',
                })
            



#Django Model Form
class TaskModelForm(StyledForMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'due_date' : forms.SelectDateWidget,
            'assigned_to' : forms.CheckboxSelectMultiple
        }
        # exclude = ['project', 'is_completed', 'created_at', 'updated_at']

        """Manual Widget"""
        # widgets={
        #     'title' : forms.TextInput(attrs = {
        #         'class' : "border-2  border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        #         'placeholder' : "Enter task title"
        #     }),
        #     'description' : forms.Textarea(attrs = {
        #         'class' : "border-2  border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
        #         'placeholder' : "dscribe your about your task"
        #     }),
        #     'due_date' : forms.SelectDateWidget(attrs = {
        #         'class' : "border-2  border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
        #     }),
        #     'assigned_to' : forms.CheckboxSelectMultiple(attrs = {
        #         # 'class' : "border-2  border-gray-300 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"
        #     })
        # }

    """Using Mixin Widget"""
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.apply_styled_widget()

        
class TaskDetailModelForm(StyledForMixin, forms.ModelForm):
    
    class Meta:
        model = TaskDetail
        fields = ['priority', 'notes']

        widgets = {
            'priority' : forms.Select(),
            # 'assigned_to' : forms.CheckboxSelectMultiple
        }
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.apply_styled_widget()
