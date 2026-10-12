# 6. Ethical Hacking Note (Task 14)

**Legal limits.** Security testing is lawful only with *explicit, written authorisation* from the system owner. Without it, scanning, probing, password guessing, sniffing or exploiting is a crime under the Information Technology Act, 2000 in India (e.g. Sec. 43 unauthorised access/damage, Sec. 66 computer-related offences, Sec. 66C identity theft, Sec. 72 breach of confidentiality) and under laws such as the CFAA (USA) and the Computer Misuse Act (UK). The DPDP Act, 2023 adds duties on handling personal data found during testing. Authorisation does not cover systems outside the agreed scope, and a contract does not make illegal acts legal.

**Ethical limits.** Stay inside the agreed scope, time window and rules of engagement; avoid destructive tests (DoS, data deletion) unless approved; protect any data seen (minimise, never copy or share it); disclose findings only to the client; follow responsible/coordinated disclosure for third-party flaws; never accept payment for silence or take advantage of access.

**Role of an ethical hacker.** Thinks like an attacker to find weaknesses before criminals do: reconnaissance, scanning, vulnerability analysis, controlled exploitation to prove impact, and reporting. Differs from a black-hat (no permission, malicious intent) and from a grey-hat (no permission, maybe good intent, still unlawful).

**Responsibilities.** (1) Get a signed scope/authorisation (NDA, rules of engagement). (2) Do no harm; back up and restore. (3) Maintain confidentiality, integrity of evidence. (4) Report honestly with risk ratings and remediation advice, including what was *not* tested. (5) Remove tools/accounts, retest fixes. (6) Keep learning and follow codes of conduct (EC-Council CEH, (ISC)² ethics).

**In this project:** all testing (ping sweep, sniffing, the "attacker" PC) is performed only inside the Packet Tracer simulation. No real network, system or Wi-Fi is scanned or attacked, as required by the lab rules.
