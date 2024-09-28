from django.db import models
from django.apps import apps


class ApprovalHistory(models.Model):
    application = models.ForeignKey('app.Application', related_name='approval_history', on_delete=models.CASCADE)
    executor_moderator = models.ForeignKey('Moderator', on_delete=models.SET_NULL, null=True, blank=True)
    executor_bank_secretary = models.ForeignKey('BankSecretary', on_delete=models.SET_NULL, null=True, blank=True)
    executor_bank_council = models.ForeignKey('BankCouncil', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    date_of_action = models.DateTimeField(auto_now_add=True)  # Automatically set on record creation

    def __str__(self):
        return f"{self.application} - {self.status} by {self.get_executor_display()}"

    def get_executor_display(self):
        if self.executor_moderator:
            return f"Moderator: {self.executor_moderator}"
        elif self.executor_bank_secretary:
            return f"Bank Secretary: {self.executor_bank_secretary}"
        elif self.executor_bank_council:
            return f"Bank Council: {self.executor_bank_council}"
        return "Unknown"