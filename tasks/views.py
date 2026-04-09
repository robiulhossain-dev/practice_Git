from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee,Task, TaskDetail
# Create your views here.

def home(request):
    return render(request,"home.html")


def manager_dashboard(request):
    return render(request,"dashboard/manager_dashboard.html")


def user_dashboard(request):
    return render(request,"dashboard/user_dashboard.html")


def test(request):
    context = {
        "names" : ["rana", "ahmed", "emon",18]
    }
    return render(request, "test.html", context)


def create_task(request):
    # employees = Employee.objects.all()
    form = TaskModelForm()

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        print(form)
        if form.is_valid():
            """For Model Form Data"""
            form.save()
            return render(request, "task_form.html", {"form":form, "message":"Task Added Successfully"})
            """For Django Form Data"""
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')

            # task = Task.objects.create(
            #     title=title,
            #     description=description,
            #     due_date=due_date)

            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # return HttpResponse("Task Added Successfully")

    context = { 
        "forms" : form
    }
    return render(request, "task_form.html", context)


def view_task(request):
    # tasks = TaskDetail.objects.all()
    # tasks = Task.objects.select_related("details").all()
    tasks = TaskDetail.objects.select_related("task").all()
    return render(request, "show_task.html", {"tasks" : tasks})