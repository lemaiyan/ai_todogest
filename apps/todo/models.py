from datetime import datetime, timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from structlog import get_logger
from tinymce.models import HTMLField

from apps.integrations import calendar, chatgpt

logger = get_logger()


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Priority(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Priorities'


class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(default=datetime.now() + timedelta(days=2), blank=True, null=True)
    start_date = models.DateTimeField(default=datetime.now() + timedelta(days=1), blank=True, null=True)
    end_date = models.DateTimeField(default=datetime.now() + timedelta(days=1,hours=1), blank=True, null=True)
    added_to_calendar = models.BooleanField(default=False)
    event = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ Return the string representation of the class

        :return: string
        """
        return self.title

    class Meta:
        verbose_name_plural = 'Todo Items'
        ordering = ['title']

class EmailDigest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Email Summary'
        ordering = ['created_at']

@receiver(post_save, sender=TodoItem)
def create_user_profile(sender, instance, created, **kwargs):
    logger.info("starting post_save")
    if created:
        logger.info("created", instance=instance.title)
        task_fetch_content.apply_async(args=(instance.title, instance.id),
                                                       queue='chatgpt_fetch_content')
    logger.info("end post_save")



@shared_task(name='chatgpt.fetch_content')
def task_fetch_content(prompt, todo_item_id):
    logger.info("starting task-fetch-content")
    p = chatgpt.Preprocess()
    content = p.prompt(prompt)
    todo_item = TodoItem.objects.get(id=todo_item_id)
    todo_item.content = content
    todo_item.completed = True
    todo_item.save()
    logger.info("task-fetch-content", content=content, todo=todo_item.title)
    logger.info("ending task-fetch-content")
    task_add_to_calendar.apply_async(args=(todo_item.id,), queue='calendar_add_to_calendar')

@shared_task(name='chatgpt.add_to_calendar')
def task_add_to_calendar(todo_item_id):
    logger.info("starting task-add-to-calendar")
    todo_item = TodoItem.objects.get(id=todo_item_id)
    cal=calendar.Calendar(todo_item.user.email)
    if todo_item.start_date is None or todo_item.end_date is None or todo_item.completed is False:
        logger.info("task-add-to-calendar", todo=todo_item.title, added=False, 
                    reason="start_date or end_date is None or completed is False", 
                    start_date=todo_item.start_date, end_date=todo_item.end_date, 
                    completed=todo_item.completed)
        return
    content = todo_item.content
    if "I am unable" in content or "I am not able" in content:
        content = todo_item.title
    added, event = cal.add_event(todo_item.title, todo_item.start_date, todo_item.end_date, content, todo_item.user.email)
    if added:
        todo_item.added_to_calendar = True
        todo_item.event = event
        todo_item.save()
    logger.info("task-add-to-calendar", todo=todo_item.title, added=added)
    logger.info("ending task-add-to-calendar")