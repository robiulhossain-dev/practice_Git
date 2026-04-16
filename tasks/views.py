from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee,Task, TaskDetail
from django.db.models import Q, Count
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request,"home.html")


def manager_dashboard(request):
    # type = request.GET.get('type')
    # tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all() 
    # total_tasks = tasks.count()
    # completed_tasks = Task.objects.filter(status = "COMPLETED").count()
    # pending_tasks = Task.objects.filter(status = "PENDING").count()
    # progress_tasks = Task.objects.filter(status = "IN_PROGRESS").count()

    counts = Task.objects.aggregate(
        total_tasks = Count('id'),
        completed_tasks = Count('id', filter=Q(status='COMPLETED')),
        pending_tasks = Count('id', filter=Q(status='PENDING')),
        progress_tasks = Count('id', filter=Q(status='IN_PROGRESS')),
    )

    type = request.GET.get('type')
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    
    if type == "completed":
            tasks = base_query.filter(status="COMPLETED") 
    elif type == "pending":
            tasks = base_query.filter(status="PENDING") 
    elif type == "in_progress":
            tasks = base_query.filter(status="IN_PROGRESS") 
    else:
            tasks = base_query.all()


    context = {
        "tasks" : tasks,
        "counts" : counts
        # "total_tasks" : total_tasks,
        # "completed_tasks" : completed_tasks,
        # "pending_tasks" : pending_tasks,
        # "progress_tasks" : progress_tasks
    }
    return render(request,"dashboard/manager_dashboard.html", context)


def user_dashboard(request):
    return render(request,"dashboard/user_dashboard.html")


def test(request):
    context = {
        "names" : ["rana", "ahmed", "emon",18]
    }
    return render(request, "test.html", context)


def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()
    taskdetail_form = TaskDetailModelForm()
    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        taskdetail_form = TaskDetailModelForm(request.POST)
        # print(form)
        if task_form.is_valid() & taskdetail_form.is_valid():
            """For Model Form Data"""
            task = task_form.save()
            task_detail = taskdetail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Succesfully")
            return redirect("create-task")
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
        "task_form" : task_form,
        "taskdetail_form" : taskdetail_form
    }
    return render(request, "task_form.html", context)



def update_task(request, id):
    # employees = Employee.objects.all()
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)
    if task.details:
        taskdetail_form = TaskDetailModelForm(instance=task.details)

    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        taskdetail_form = TaskDetailModelForm(request.POST, instance=task.details)
        # print(form)
        if task_form.is_valid() & taskdetail_form.is_valid():
            """For Model Form Data"""
            task = task_form.save()
            task_detail = taskdetail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task updated Succesfully")
            return redirect("update-task", id)
            """For Django Form Data"""
            
    context = { 
        "task_form" : task_form,
        "taskdetail_form" : taskdetail_form
    }
    return render(request, "task_form.html", context)



def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id = id)
        task.delete()
        messages.success(request, "Task deleted Succesfully")
        return redirect("manager-dashboard")
    else:
        messages.error(request, "Something Went wrong")
        return redirect("manager-dashboard")

def view_task(request):
    # tasks = TaskDetail.objects.all()
    # tasks = Task.objects.select_related("details").all()
    # tasks = TaskDetail.objects.select_related("task").all()
    # tasks = Task.objects.filter(title__icontains="p")
    # tasks = Task.objects.filter(Q(status="PENDING") | Q(status="IN_PROGRESS"))
    task_count = Task.objects.aggregate(num_task = Count('id'))

    return render(request, "show_task.html", {"task_count" : task_count})