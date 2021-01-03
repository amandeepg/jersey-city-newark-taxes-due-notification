# Jersey City & Newark Property Tax Due Notifier

Self-hosted script to check if tax is due soon for a particular account for a property in [Jersey City, NJ](https://www.google.com/maps/place/Jersey+City,+NJ) or [Newark, NJ](https://www.google.com/maps/place/Newark,+NJ), and will send you an email.

Designed to run on a FaaS provider, specifically [Google Cloud Functions](https://cloud.google.com/functions/) (but will probably work with modifications on others like [Amazon AWS Lambda](https://aws.amazon.com/lambda/), [CloudFlare Workers](https://workers.cloudflare.com/), [Microsoft Azure Functions](https://azure.microsoft.com/en-us/services/functions/), etc.)

Deploy and set it to run on a schedule. It's your responsibility to check that it continues to work without errors, watch the logs, read the code.

##### Environment variables
* `ACCOUNT_NUMBER`: Account number from http://taxes.cityofjerseycity.com/ or https://taxes.ci.newark.nj.us
* `CITY`: `Jersey City` or `Newark`
* `SENDGRID_API`: [Sendgrid](https://app.sendgrid.com)'s [API key](https://app.sendgrid.com/settings/api_keys)
* `DAYS_THRESHOLD`: How many days before a tax payment is due you want to be notified via email. Optional, default is 31 days.
* `FROM_EMAIL`: The email address Sendgrid will use to send the mail. You'll want this [verified](https://sendgrid.com/docs/for-developers/sending-email/sender-identity/) with Sendgrid.
* `TO_EMAIL`: The email address to send the notification to.
* `EMAIL_SUBJECT`: The subject of the email that will be sent.
