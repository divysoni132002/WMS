from django.db import models
from django.utils import timezone
from django.core.mail import send_mail

class Vendor(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.username

class Task(models.Model):
    username = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    task = models.CharField(max_length=200)
    hours = models.FloatField()
    status = models.CharField(max_length=50)
    dependency = models.CharField(max_length=100, blank=True, null=True)
    communication_of_change = models.CharField(max_length=100, blank=True, null=True)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.task} ({self.date})"

class Assignment(models.Model):
    TASK_CHOICES = [
        ('API_upgrade_needed', 'API upgrade needed'),
        ('New_API_needed', 'New API needed'),
        ('API_check', 'API check'),
        ('Bug_fix', 'Bug fix'),
        ('Front_end_work', 'Front end work'),
        ('Integration_work', 'Integration work'),
        ('Git_work', 'Git work'),
        ('UI_UX_work', 'UI/UX work'),
        ('Meeting_discussion', 'Meeting and discussion'),
        ('Others', 'Others'),
    ]

    task_to_work_on = models.TextField()
    type_of_task = models.CharField(max_length=20, choices=TASK_CHOICES)
    assign_to = models.ForeignKey(Vendor, related_name='assignee', on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(Vendor, related_name='assigner', on_delete=models.CASCADE)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    date_of_assignment = models.DateField()
    expected_hours_by_assigner = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    expected_hours_by_assignee = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    expected_date_of_delivery = models.DateField(blank=True, null=True)
    date_of_delivery_by_assignee = models.DateTimeField(blank=True, null=True)
    days_of_delay = models.IntegerField(null=True, blank=True)
    mark_as_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task_to_work_on} assigned to {self.assign_to}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        
        # Calculate days of delay
        if self.expected_date_of_delivery and not self.mark_as_complete:
            today = timezone.now().date()
            delay = (today - self.expected_date_of_delivery).days
            self.days_of_delay = delay if delay > 0 else 0
        else:
            self.days_of_delay = None
        
        super().save(*args, **kwargs)

        # Send email notification for new assignments
        if is_new:
            owner_email = 'rohit@unboxai.in'
            team_leader_email = 'srconsultant@unboxai.in'
            
            vendor1 = Vendor.objects.get(username=self.assigned_by.username)
            vendor2 = Vendor.objects.get(username=self.assign_to.username)
            recipient_list = [owner_email, team_leader_email, vendor1.email, vendor2.email]

            subject = f"New Task Assigned: {self.task_to_work_on}"
            message = f"Dear {self.assign_to.username},\n\nYou have been assigned a new task '{self.task_to_work_on}' by {self.assigned_by.username}. The expected date of delivery is {self.expected_date_of_delivery}.\n\nPlease review the task details and acknowledge receipt.\n\nRegards."

            try:
                send_mail(subject, message, 'cosmicwisdomyt@gmail.com', recipient_list)
            except Exception as e:
                print(f"An error occurred while sending the email to {recipient_list}: {str(e)}")

class DependencyResolution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    resolved_by = models.CharField(max_length=100)
    resolved_date = models.DateTimeField()
    dependency = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.task.task} - Resolved by {self.resolved_by}"

class EmailLog(models.Model):
    event = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    email_status = models.CharField(max_length=500)
    message = models.TextField()
    user_id = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    corporate_name = models.CharField(max_length=255, blank=True, null=True)
    corporate_phone = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class TechLog(models.Model):
    date = models.DateField()
    time = models.TimeField()
    username = models.CharField(max_length=30)
    change_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.change_type} - {self.date}"