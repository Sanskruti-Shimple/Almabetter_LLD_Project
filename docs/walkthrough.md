# LMS Capstone Walkthrough (10-12 minutes)

This is a recording script and demo checklist. Target duration: about 11 minutes. Keep the repository and terminal visible; run commands from the repository root.

## 0:00-1:00 | Problem and scope

"This project models a learning management system with learners, instructors, courses, assignments, grading, notifications, and reports. The goal is to make business rules testable and replaceable rather than putting every behavior in one manager class. This is an in-memory reference implementation, not a deployed production service."

Show the project tree and point out the `users`, `courses`, `assignments`, `grading`, `notifications`, and `reports` modules.

## 1:00-2:15 | Architecture and domain model

Open the architecture and class diagrams in `README.md`. Explain the layered modular monolith: application services coordinate domain work; repository and gateway interfaces isolate persistence and external delivery. Mention that HTTP controllers, a database, Redis, a load balancer, and a message broker are production extension points, not implemented dependencies.

Point to `User` and its role-specific subclasses, immutable `Course`, and the `Assignment` aggregate.

## 2:15-4:00 | SOLID course module

Open `lms/courses/service.py`, `repository.py`, and `models.py`.

"CourseService owns course use cases and depends on a repository contract, not the in-memory dictionary. CourseBuilder validates a course and keeps optional module construction out of the domain constructor. Course data is immutable, so enrollment creates and persists a replacement instead of mutating a shared object."

Identify SRP in service/repository separation, OCP in repository substitution, and DIP in constructor injection.

## 4:00-6:00 | Assignment State and Decorator

Open `lms/assignments/states.py`, `models.py`, and `security.py`.

"An assignment moves from draft to published to submitted to graded. State objects reject transitions that do not make sense. The aggregate lock protects each local transition. The role decorator checks the actor at the application-service boundary, so an unauthorized action fails before domain mutation."

Mention that production identity must be verified by an authentication layer; the demo role object alone is not authentication.

## 6:00-8:15 | Grading patterns

Open `lms/grading/strategies.py`, `service.py`, and `adapter.py`.

"GradingService depends on an abstract strategy. Percentage and pass/fail are interchangeable policies. The Adapter wraps a legacy four-point grade API so existing grading infrastructure can be reused without changing the new service contract."

Point out Decimal-based grade calculations and invalid score validation.

## 8:15-9:45 | Notification patterns

Open `lms/core/events.py`, `lms/notifications/factory.py`, `channels.py`, and `observers.py`.

"Submission publishes an event. The observer sends a confirmation without the assignment service knowing about email. The factory chooses a sender, the Bridge separates sender from channel, and the SMS Adapter translates an older API. In production, a durable outbox and broker would replace this in-process event bus."

## 9:45-10:45 | Run the demo and tests

In the terminal run:

```powershell
python -m unittest discover -v
python -m lms
```

Show that the tests run without network services and that the demo prints notification delivery, grade, and course summary output.

## 10:45-11:30 | Scale, caveats, and close

"The reference repositories use locks only within one process. For multiple API instances, persistence transactions, optimistic versioning, idempotency keys, and a durable event outbox are needed. Course metadata can use cache-aside with TTL and invalidation; private submissions and authorization decisions need careful cache boundaries. Stateless API replicas sit behind a health-checked load balancer."

Close with the three smells and their refactorings in the README: god service, conditional grading, and contradictory lifecycle flags. State clearly that scalability is documented as a blueprint and was not benchmarked or deployed.
