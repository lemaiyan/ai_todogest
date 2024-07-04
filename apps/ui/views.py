from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from structlog import get_logger
from apps.oauth.models import GoogleUser
from apps.todo.models import Category, Priority, TodoItem, EmailDigest
log = get_logger()

class LoginView(TemplateView):
    template_name = "login.html"
    
 
class UserTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if (
                not request.user.is_authenticated
                or not request.user.is_active
        ):
            return redirect("apps.ui:login")
        else:
            return super().get(request, *args, **kwargs)  

class DashboardView(UserTemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # get to do that are not completed
        context['not_complete'] = TodoItem.objects.filter(user=user, completed=False)
        context['not_complete_count'] = TodoItem.objects.filter(user=user, completed=False).count()
        context['todos'] = TodoItem.objects.filter(user=user)
        context['todos_count'] = TodoItem.objects.filter(user=user).count()
        # get email digests
        context['email_digests'] = EmailDigest.objects.filter(user=user)
        context['email_digests_count'] = EmailDigest.objects.filter(user=user).count()
        return context
   

class DeleteTaskView(UserTemplateView):
    template_name = "tasks.html"
    
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id', 0)
        user = request.user
        TodoItem.objects.filter(id=task_id, user=user).delete()
        messages.success(request, "Task deleted successfully")
        return redirect(reverse("apps.ui:tasks"))

class DeleteEmailDigestView(UserTemplateView):
    template_name = "mailbox.html"
    
    def get(self, request, *args, **kwargs):
        email_id = kwargs.get('email_id', 0)
        user = request.user
        EmailDigest.objects.filter(id=email_id, user=user).delete()
        messages.success(request, "Email deleted successfully")
        return redirect(reverse("apps.ui:mailbox"))

class TaskView(UserTemplateView):
    template_name = "tasks.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['categories'] = Category.objects.all()
        context['priorities'] = Priority.objects.all()
        context['todos'] = TodoItem.objects.filter(user=user)
        return context
    
class AddTaskView(UserTemplateView):
    template_name = "addtask.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['categories'] = Category.objects.all()
        context['priorities'] = Priority.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        user = request.user
        title = request.POST.get('title', '')
        category_id = request.POST.get('category', '')
        priority_id = request.POST.get('priority', '')
        category = Category.objects.get(id=category_id)
        priority = Priority.objects.get(id=priority_id)
        todo_item = TodoItem.objects.create(
            user=user,
            title=title,
            category=category,
            priority=priority
        )
        messages.success(request, "Task added successfully")
        return redirect(reverse("apps.ui:tasks"))
    
    

class ProfileView(UserTemplateView):
    template_name = "profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        google_user = get_google_user(user)
        context['google_user'] = google_user
        log.info("Google user", google_user=google_user)
        return context
        
    
class DigestView(UserTemplateView):
    template_name = "mailbox.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['email_digests'] = EmailDigest.objects.filter(user=user)
        return context
    
class ReadDigestView(UserTemplateView):
    template_name = "readmail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email_id = kwargs.get('email_id', 0)
        user = self.request.user
        context['email'] = EmailDigest.objects.get(id=email_id)
        return context
    

def get_google_user(user):
    try:
        return GoogleUser.objects.get(user=user)
    except GoogleUser.DoesNotExist:
        return None