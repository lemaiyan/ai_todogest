from apps.ui.views import (LoginView, DashboardView, TaskView, AddTaskView, ProfileView, DigestView,
                           ReadDigestView,DeleteTaskView, DeleteEmailDigestView,
                           ViewTaskView)
from django.urls import path
app_name = "apps.ui"

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("tasks/", TaskView.as_view(), name="tasks"),
    path("task/<int:task_id>", ViewTaskView.as_view(), name="task"),
    path("addtask/", AddTaskView.as_view(), name="addtask"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("mailbox/", DigestView.as_view(), name="mailbox"),
    path("readmail/<email_id>", ReadDigestView.as_view(), name="readmail"),
    path("deletetask/<task_id>", DeleteTaskView.as_view(), name="deletetask"),
    path("deletemail/<email_id>", DeleteEmailDigestView.as_view(), name="deletemail"),
]