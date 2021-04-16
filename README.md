# scrumnest-api

Backend GraphQL API for [ScrumNest.com](https://scrumnest.com)

## Local Deployment

1. Make sure you have an AWS Account and Access Keys
2. Serverless
3. Python 3.8

### Important

Make sure that you have an email address verified in AWS SES (Simple Email Service).

You will need this email to deploy

### Serverless Deploy

```bash
serverless deploy --email <your email>
```

Example:
```bash
serverless deploy --email email@example.com
```
