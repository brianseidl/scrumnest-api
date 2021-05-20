# scrumnest-api

Backend GraphQL API for [ScrumNest.com](https://scrumnest.com)

## Local Deployment

1. Make sure you have an AWS Account and Access Keys
2. Serverless
3. Python 3.8
4. NPM package manager

### Installing Dependencies

#### Serverless

```bash
npm install -g serverless
```

#### NPM Dependencies

```bash
npm install
```

#### Python Dependencies

If you are not deploying from a unix machine, you may need to install python requirements

```bash
pip3 install -r requirements.txt
```

### Exporting AWS Credentials

In order to deploy this serverless application from your local CLI, you will need to create a user for yourself and generate Access Keys. A more detailed guide can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Once you have generated your tokens, you will need to export them in your CLI.

```bash
export AWS_ACCESS_KEY_ID=********************
export AWS_SECRET_ACCESS_KEY=****************************************
export AWS_DEFAULT_REGION=us-east-1
```

### Important

Make sure that you have an email address verified in AWS SES (Simple Email Service). More information can be found [here](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html).

You will need to provide this email to deploy your serverless application.

### Serverless Deploy

```bash
serverless deploy --email <your email>
```

Example:
```bash
serverless deploy --email email@example.com
```

### Removing Serverless

If you choose to take down your application, you can do by running
```bash
serverless remove
```

### Running Tests

```bash
nosetests --logging-level=INFO
```
