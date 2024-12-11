from .utils import send_email_to_user, save_email_to_csv

@api_view(['POST'])
def create_transaction(request):
    data = request.data
    email = data.get('email')
    amount = data.get('amount')
    transaction_type = data.get('transaction_type')
    description = data.get('description')

    # Validate email format
    if not email or "@" not in email or "." not in email:
        return Response({"error": "Invalid email address"}, status=400)

    # Save transaction to DB
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
        f"Your account has been {transaction_type}ed with {amount}.\n\n"
        f"Details:\nDescription: {description}\nAmount: {amount}\n\n"
        f"Thank you for using our service.\n"
    )

    # Send email and get headers
    email_headers = send_email_to_user(email, subject, body)

    # Save email headers to CSV
    save_email_to_csv(
        email=email,
        subject=email_headers['Subject'],
        from_email=email_headers['From'],
        to_email=email_headers['To'],
        date=email_headers['Date'],
        message_id=email_headers['Message-ID'],
        body=body
    )

    return Response({"message": "Transaction recorded and email sent successfully."})
