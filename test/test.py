
import mptemail

result = mptemail.sendEmail(
    subject="test email service", 
    message="helloworld, this email service", 
    emails=["xxx@yyy.com"],
    host="http://10.16.2.16:8002",
    api_key="8M2ZBv9u.xxx",
    ssl_verify=False
)
print(result)