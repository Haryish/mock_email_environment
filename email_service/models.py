from django.db import models

class Transaction(models.Model):
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10)  # 'debit' or 'credit'
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the date when created

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.email}"


class EmailLog(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.email} at {self.timestamp}"

