from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Transaction, EmailLog
from .utils import write_to_csv

@api_view(['POST'])
def create_transaction(request):
    data = request.data
    email = data.get('email')
    amount = data.get('amount')
    transaction_type = data.get('transaction_type')
    description = data.get('description')

    if not email or "@" not in email:
        return Response({"error": "Invalid email address"}, status=400)

    # Save transaction to the database
    transaction = Transaction.objects.create(
        email=email,
        amount=amount,
        transaction_type=transaction_type,
        description=description,
    )

    # Prepare email content
    subject = f"Transaction Notification: {transaction_type.capitalize()}"
    body = (
        f"Dear User,\n\n"
        f"Your account has been {transaction_type}ed with {amount}.\n"
        f"Description: {description}\n\n"
        f"Thank you for using our service."
    )

    # Send email
    try:
        send_mail(
            subject,
            body,
            'your-email@gmail.com',  # Replace with your Gmail address
            [email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({"error": "Failed to send email", "details": str(e)}, status=500)

    # Log the email and save transaction to CSV
    EmailLog.objects.create(email=email, subject=subject, body=body)
    write_to_csv(email, {
        "transaction_id": transaction.id,
        "amount": amount,
        "transaction_type": transaction_type,
        "description": description,
        "date": transaction.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    })

    return Response({"message": "Transaction recorded and email sent successfully."})
