```sequence
User->Frontend: Create Account
Frontend->Orchestrator: Create Account DTO
Orchestrator->Account Service: email/password
Account Service-->Orchestrator: account UUID
Account Service->SES: Confirm Registration UUID
SES-->User: Confirmation email link (http://.../confirm/UUID)
Orchestrator->Customer Service: Create Customer DTO
Customer Service-->Orchestrator: Customer Record
Orchestrator-->Frontend: Customer Record
Frontend-->User: Customer Profile
User->Orchestrator: Click email confirmation
Orchestrator->Account Service: /confirm/UUID
```