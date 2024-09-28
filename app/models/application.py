from datetime import timezone
from django.db import models
from django.apps import apps
from .projects import Project
from .bank_council import BankMember, Criteria


class Application(models.Model):
    STATUS_CHOICES = [
        ('under_review', 'Under Review'),
        ('returned_for_revision', 'Returned for Revision'),
        ('approved_by_moderator', 'Approved by Moderator'),
        ('approved_by_bank_secretary', 'Approved by Bank Secretary'),
        ('rejected', 'Rejected'),
        ('visible', 'Visible to Users'),
    ]

    project = models.ForeignKey(Project, related_name='applications', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    submission_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    current_checker = models.ForeignKey("user.CustomUser", on_delete=models.SET_NULL, null=True, blank=True, related_name='current_checker')

    def __str__(self):
        return f"Application for {self.project.startup_name} - {self.get_status_display()}"

    def create_approval_history(self, executor, status, comment=None):
        ApprovalHistory = apps.get_model('app', 'ApprovalHistory')
        ApprovalHistory.objects.create(
            application=self,
            executor_moderator=executor.moderator if hasattr(executor, 'moderator') else None,
            executor_bank_secretary=executor.banksecretary if hasattr(executor, 'banksecretary') else None,
            executor_bank_council=executor.bankcouncil if hasattr(executor, 'bankcouncil') else None,
            status=status,
            comment=comment,
            date_of_action=timezone.now(),
        )

    def calculate_average_score(self):
        # Get all scores for the application
        scores = ApplicationScore.objects.filter(application=self)

        # Calculate the average score for each criteria
        criteria_scores = {}
        for score in scores:
            if score.criteria_score:  # Ensure criteria is not None
                criteria_id = score.criteria_score.id
                if criteria_id not in criteria_scores:
                    criteria_scores[criteria_id] = []
                criteria_scores[criteria_id].append(score.score)

        # Calculate the overall average score across all criteria
        total_average_score = 0
        for criteria_id, scores_list in criteria_scores.items():
            total_average_score += sum(scores_list) / len(scores_list)

        overall_average = total_average_score / len(criteria_scores) if criteria_scores else 0

        # Update application status based on the overall average score
        if overall_average >= 9:
            self.status = 'visible'
        else:
            self.status = 'rejected'

        self.save()
        return overall_average


class ApplicationScore(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='scores')
    member = models.ForeignKey(BankMember, on_delete=models.CASCADE, related_name='application_scores')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    criteria_score = models.ForeignKey(Criteria, on_delete=models.SET_NULL, blank=True, null=True)

    
    def __str__(self):
        return f"{self.application.project.startup_name} - {self.score}"


class ApplicationNotification(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    company_owner_first_name = models.CharField(max_length=255)
    company_owner_last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.project_name} - {self.company_owner_first_name} {self.company_owner_last_name}"