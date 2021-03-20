```sequence
User->Customer Service: Request account deletion
Customer Service->Account Service: Initiate Delete (customerId)
Account Service->RDS: Create deletion token (deletionToken)
Account Service->Email Service: Send Deletion Email (deletionToken)
Email Service-->User: Confirm delete account (deletionUrl)
User->Customer Service: Confirm Delete account (email, password, token)
Customer Service->Account Service: Delete account (email, password, deleteToken)
Account Service->RDS: Retrieve authentication
RDS-->Account Service: Check authentication
Account Service->RDS: Get deletion token
RDS-->Account Service: Validate token
Account Service->RDS: Delete (accountId)
Account Service-->Customer Service: Account deleted (accountId)
Customer Service->RDS: Delete customer (customerId)
Customer Service-->User: Account deleted
```