# AED Guardian AI — Safety and Privacy Compliance

## Lane

Lane 3 — Registry and readiness

## Prototype Boundary

AED Guardian AI is a registry-quality decision-support prototype.

It is intended for:

- Planning
- Registry analysis
- Data-quality review
- Human-in-the-loop validation
- Historical or synthetic demonstrations

It is NOT an emergency-response system.

---

# Mandatory Emergency-Use Notice

**Prototype for planning and simulation only — not for emergency use.**

**In an emergency in Singapore, call 995 immediately and follow SCDF
instructions. Use official SCDF/myResponder channels. Do not delay emergency
action to use this prototype.**

This notice must be displayed on every user-facing demonstration screen.

---

# 1. Live Emergency Boundary

The prototype does NOT provide:

- Live incident reporting
- Emergency dispatch
- Responder alerts
- Ambulance routing
- SCDF integration
- 995 integration
- myResponder integration
- National AED registry integration

Only scripted, historical, or synthetic scenarios are permitted for demonstrations.

---

# 2. AED Readiness Boundary

The supplied registry dataset does not contain live device-health information.

Therefore the prototype does NOT claim to detect:

- Depleted batteries
- Expired pads
- Failed inspections
- Maintenance failures
- Physical AED removal
- Current device readiness
- Current operational status

A registry record is NOT proof that an AED is currently:

- Present
- Accessible
- Working
- Inspected
- Ready for use

`OPERATING_HOURS` is treated as registry text and not as a guarantee of
current access.

---

# 3. Data-Quality Boundary

A system flag represents a possible data-quality concern.

It does NOT automatically represent a confirmed real-world fault.

For example:

Two AED records may have identical coordinates while legitimately describing
different floors or indoor locations.

Therefore the system sends such cases to human review rather than automatically
merging or deleting records.

---

# 4. Human-in-the-Loop Safety

The duplicate review interface provides three outcomes:

- `DUPLICATE`
- `NOT_DUPLICATE`
- `UNCERTAIN`

The `UNCERTAIN` state allows the reviewer to abstain when the available
evidence is insufficient.

The system does not force an unsupported binary decision.

---

# 5. Safe Failure States

The prototype uses conservative behavior when information is insufficient.

Examples include:

### Missing operating hours

Classify as:

`MISSING`

with LOW confidence.

### Unusual operating-hours text

Classify as:

`AMBIGUOUS`

and allow further review.

### Potential duplicate with conflicting indoor descriptions

Surface the candidate for human review.

### Insufficient evidence

Allow:

`UNCERTAIN`

rather than asserting a definitive result.

---

# 6. Dataset and Uncertainty Disclosure

The prototype uses a historical AED registry snapshot.

The interface and documentation must make clear:

- Dataset date
- Supplemental-source dates, if any
- Assumptions
- Uncertainty
- Known failure modes

The system must not present historical registry information as live readiness
information.

---

# 7. Privacy

The prototype does not require collection of:

- Names
- Contact details
- Health information
- Responder identities
- Patient information
- Emergency incident information
- Precise participant-location history

Public demonstrations should use synthetic start points whenever possible.

No individual medical risk or household-level risk is inferred.

---

# 8. Location Data

The registry contains AED coordinates because they are part of the supplied
public dataset.

The prototype does not collect participant location history as part of the
Lane 3 workflow.

If any future demonstration requires participant device-location data:

- Obtain informed consent.
- Collect only what is necessary.
- Protect data in transit.
- Protect data at rest.
- Delete the data after the session.

---

# 9. Security

The prototype must not expose:

- Private API keys
- Credentials
- Authentication tokens
- Secrets

Credentials must not be committed to the repository or included in:

- Logs
- Screenshots
- Presentation material
- Generated reports

---

# 10. Synthetic and Historical Data

Only the supplied historical registry data and appropriately documented
synthetic scenarios are used for the judged demonstration.

Synthetic data must be clearly labelled as synthetic and must not be presented
as observed real-world events.

No live SCDF incident or private responder data is used.

---

# 11. Known Limitations

The prototype cannot determine from the supplied registry alone:

- Whether an AED is currently installed
- Whether an AED is accessible right now
- Whether an AED is operational
- Whether batteries are charged
- Whether pads are expired
- Whether an inspection was completed
- Whether a temporary closure exists
- Whether a physical route is currently unobstructed

These limitations are part of the safety boundary and must remain visible in
the final demonstration.

---

# 12. Safety Gate Checklist

| Requirement | Status |
|---|---|
| Planning/simulation boundary | PASS |
| Emergency-use warning | PASS |
| No live incident integration | PASS |
| No dispatch/alerts | PASS |
| No medical diagnosis | PASS |
| No unsupported AED readiness claims | PASS |
| Historical dataset disclosed | PASS |
| Safe uncertainty state | PASS |
| Human review required for duplicate decisions | PASS |
| Synthetic scenarios permitted | PASS |
| No patient/responder data | PASS |
| No participant location history | PASS |
| Credentials excluded | PASS |

---

# Final Safety Statement

AED Guardian AI is a registry-quality decision-support prototype.

It identifies possible data-quality concerns and routes uncertain cases to a
human reviewer.

It does not determine current AED readiness and must not be used during an
emergency.

**Prototype for planning and simulation only — not for emergency use.**

**In an emergency in Singapore, call 995 immediately and follow SCDF
instructions. Use official SCDF/myResponder channels. Do not delay emergency
action to use this prototype.**

Generated: August 2026
