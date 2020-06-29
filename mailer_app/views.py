import os
import sendgrid
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from sendgrid.helpers.mail import (Mail,
                                   Email,
                                   Personalization
                                   )
from python_http_client import exceptions
from rest_framework.response import Response
from twilio_sendgrid_integration.settings import DEFAULT_FROM_EMAIL, SENDGRID_API_KEY

sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)


class MailSenderAPIView(GenericAPIView):
    def send_mail(self, template_id, sender, recipient, data_dict):
        mail = Mail()
        mail.template_id = template_id

        mail.from_email = Email(sender)
        personalization = Personalization()
        personalization.add_to(Email(recipient))
        personalization.dynamic_template_data = data_dict
        mail.add_personalization(personalization)

        try:
            response = sg.client.mail.send.post(request_body=mail.get())
        except exceptions.BadRequestsError as e:
            print("INSIDE")
            print(e.body)
            exit()
        print(response.status_code)
        print(response.body)
        print(response.headers)

    def post(self, request):
        recepient_email = request.data['recepient_email']
        subject = request.data['subject']
        fullname = request.data['fullname']
        body = request.data['body']

        template_id = "d-1772e8ac6b5442e68975394ea71a4957"
        sender = DEFAULT_FROM_EMAIL
        data_dict = {"subject": subject, "user_name": fullname, "body": body}
        MailSenderAPIView.send_mail(self, template_id, sender, recepient_email, data_dict)

        return Response({"status_code": status.HTTP_200_OK, "message": "Mail sent successfully."})