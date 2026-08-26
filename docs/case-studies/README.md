# Case studies

The notebooks teach one skill at a time. These case studies do the opposite:
they take **one realistic scenario end to end** and show how the skills combine
under real constraints — the customer's fuzzy ask, a budget, a deadline, an
SLA, and the thing breaking two weeks after launch.

They are **reading, not exercises** — worked narratives, not new code to run.
The runnable code lives in the sections each case links back to. Read a case
before you start the [capstone](../../12-capstone/README.md): it's the shape of
what you're about to build, and of the interview round that probes it.

Each case is organized on two axes so they cover *different application types*,
not three variations of one:

| Case | Use case | Application type | The angle it teaches |
|---|---|---|---|
| [A — Customer-support assistant](A-customer-support-assistant.md) | Customer support | RAG + agent, **build → debug** | Scoping a fuzzy ask into a deployed, evaluated system — then diagnosing it when quality collapses |
| C — Contract extraction *(planned)* | Document processing | **Pipeline vs agent** | The judgment call: when a pipeline beats an agent, argued with eval + cost |
| D — Red-team benchmark *(planned)* | Security / evaluation | **Adversarial harness** | Building a harness to *evaluate and attack* models, not serve one |

> **⭐ Key takeaway —** interviews and real work never hand you "implement a RAG
> pipeline." They hand you "our support team is drowning — help." The gap between
> those two sentences is the job. These cases live in that gap.
