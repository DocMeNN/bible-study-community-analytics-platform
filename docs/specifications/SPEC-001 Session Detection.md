# SPEC-001 — Session Detection Specification

## Status

Under Review — CP-014

## Date

24 July 2026

## Purpose

This specification defines how the Online Bible Study Attendance and Participation Analytics Platform identifies Daily Sessions from WhatsApp exports.

---

# 1. Core Concept

The atomic unit of analysis is the:

Daily Session

A Daily Session represents one Bible study reading cycle beginning with the posting of the Scripture Reading activity.

The system must identify the beginning of each session reliably from real-world WhatsApp message data.

---

# 2. Session Start Definition

A Daily Session begins when a valid Scripture Reading message is posted.

The session start is therefore based on the WhatsApp message timestamp of the Scripture Reading activity.

The session identity includes the written reading date contained in the Scripture Reading message.

These are separate concepts.

---

# 3. Date Model

## 3.1 Message Timestamp

Example:

[1/1/2023, 1:03:34 PM]

This is the time the WhatsApp message was posted.

It establishes:

- Scripture Reading Activity Timestamp.
- Session Start Timestamp.

---

## 3.2 Written Reading Date

Example:

SUNDAY 1ST OF JANUARY 2023

This identifies the Bible reading date associated with the session.

It is session metadata.

---

## 3.3 Date Difference

The following is valid:

Message Timestamp:
31 December 2022

Written Reading Date:
1 January 2023

The difference does not invalidate the session.

The session begins when the Scripture Reading message is posted.

---

# 4. Scripture Reading Marker

The exact phrase:

SCRIPTURE READING

is not mandatory.

The system must recognize the actual Scripture Reading structure used in the WhatsApp group.

A valid marker must contain or be associated with:

Day of Week
+
Calendar Day
+
Month
+
Year
+
Bible Reading Reference

The exact wording may vary.

---

# 5. Day-of-Week Recognition

The following day names must be recognized:

MONDAY
TUESDAY
WEDNESDAY
THURSDAY
FRIDAY
SATURDAY
SUNDAY

Recognition must be case-insensitive.

---

# 6. Calendar-Day Recognition

The parser must support ordinal day forms.

Examples:

1ST
2ND
3RD
4TH
5TH
6TH
7TH
8TH
9TH
10TH
11TH
12TH
13TH
14TH
15TH
16TH
17TH
18TH
19TH
20TH
21ST
22ND
23RD
24TH
25TH
26TH
27TH
28TH
29TH
30TH
31ST

The parser should also support reasonable variations in formatting where the same date is represented without the ordinal suffix.

---

# 7. Month Recognition

The parser must recognize:

JANUARY
FEBRUARY
MARCH
APRIL
MAY
JUNE
JULY
AUGUST
SEPTEMBER
OCTOBER
NOVEMBER
DECEMBER

Recognition must be case-insensitive.

---

# 8. Year Recognition

The parser must recognize valid four-digit years.

Examples:

2023
2024
2025
2026

---

# 9. Bible Reading Recognition

A Scripture Reading marker must contain at least one recognizable Bible book and reading reference.

Examples:

GENESIS 1-2
MATTHEW 1
EXODUS 3-5
PSALMS 23
ROMANS 8

Supported reference patterns should include:

- Book + Chapter.
- Book + Chapter Range.
- Book + Chapter:Verse.
- Book + Chapter:Verse-Verse.
- Multiple Bible Book References.

Example:

GENESIS 1-2
MATTHEW 1

represents one Scripture Reading activity containing multiple reading references.

---

# 10. Contiguous Reading Block

The Scripture Reading marker may span multiple contiguous messages.

Example:

Message 1:
FIRST SCRIPTURE ON FOR THE YEAR 2023...SUNDAY 1ST OF JANUARY 2023

Message 2:
GENESIS 1-2

Message 3:
MATTHEW 1

The detection system must be able to associate the reading-date message with the immediately related Bible references when the group format requires multiple messages.

The implementation must define the maximum valid association boundary.

Unrelated conversation must not be incorrectly absorbed into the Scripture Reading marker.

---

# 11. Session Boundary

The session sequence is:

Message A
Message B
Scripture Reading Message
        ↓
    Session Begins
        ↓
Message C
Message D
Message E
        ↓
Next Scripture Reading Message
        ↓
Previous Session Ends
Next Session Begins

The implementation must preserve chronological ordering.

---

# 12. Expected Annual Session Count

For a complete 365-day study program:

Expected Scripture Reading Activities ≈ 365
Expected Daily Sessions ≈ 365

This is an expected business-domain validation target.

The system should not blindly force the result to 365.

Instead, it should report actual detection results and allow investigation of discrepancies.

Example:

Expected:
365

Detected:
362

Possible explanations include:

- Missed recognition variation.
- Missing WhatsApp export data.
- Duplicate or malformed marker.
- Date-range limitation.
- Incomplete study period.
- Actual missing Scripture Reading activity.

---

# 13. Iterative Session Processing

The system should support processing sessions iteratively.

Conceptual workflow:

Filtered Messages
        ↓
Find Next Valid Scripture Reading Marker
        ↓
Create Session
        ↓
Collect Messages Until Next Marker
        ↓
Analyze Session
        ↓
Repeat

This approach is preferred over treating the entire WhatsApp export as one large analysis unit.

The approach supports:

- Large exports.
- Reduced memory pressure.
- Reduced AI context pressure.
- Session-level analytics.
- Incremental processing.
- Easier error isolation.

---

# 14. Timeline Selection

The user must be able to select a specific analysis period.

Required inputs:

Start Date
End Date

The system should then process only the requested analysis period.

Conceptually:

Full WhatsApp Export
        ↓
User Selects Start Date
        ↓
User Selects End Date
        ↓
Filter Relevant Messages
        ↓
Detect Scripture Reading Markers
        ↓
Build Sessions
        ↓
Analyze Sessions

---

# 15. Timeline Boundary Concern

The following must be explicitly preserved:

Written Reading Date

and:

WhatsApp Message Timestamp

may not be the same date.

Therefore, the date-range filtering design must not accidentally exclude valid session markers simply because the message timestamp and written reading date cross a date boundary.

The final implementation must define whether the selected timeline represents:

1. Message posting time.
2. Written reading date.
3. Session identity date.
4. A combination of these.

The selected semantic must be consistent throughout:

Import
→
Session Detection
→
Analytics
→
Reports

---

# 16. Required Future Validation

The implementation must be tested against real-world examples.

## Example A — Same Date

Message Date:
1 January 2023

Written Reading Date:
Sunday 1st of January 2023

Expected:

Valid Scripture Reading Marker
New Session

---

## Example B — Message Posted Before Reading Date

Message Date:
31 December 2022

Written Reading Date:
Sunday 1st of January 2023

Expected:

Valid Scripture Reading Marker
New Session

The date mismatch must not invalidate the marker.

---

## Example C — Alternative Wording

FIRST SCRIPTURE ON FOR THE YEAR 2023...
SUNDAY 1ST OF JANUARY 2023

followed by:

GENESIS 1-2
MATTHEW 1

Expected:

Valid Scripture Reading Marker
New Session

---

## Example D — Ordinary Bible Discussion

A normal conversation message mentioning:

Genesis
Matthew
Sunday

but not representing the group's Scripture Reading announcement must not automatically create a new session.

---

# 17. Detection Principle

The system must prioritize:

Business Meaning

over:

Exact String Matching

The parser should recognize the group's real Scripture Reading communication pattern.

It must not rely on a single exact phrase when the source data demonstrates legitimate variation.

---

# 18. Current Status

This specification is under review during:

CP-014 — Presentation Layer Completion & Integration Review

The specification must be reconciled with the current implementation before code changes are made.

---

# 19. Authoritative Rule

A Daily Session begins when a valid Scripture Reading message is posted.

The Scripture Reading marker is recognized by the group's identifiable reading-announcement structure, including:

Day of Week
+
Written Calendar Date
+
Month
+
Year
+
Bible Reading Reference

The WhatsApp message timestamp establishes when the Scripture Reading activity occurred and therefore establishes the session boundary.

The written date identifies the reading associated with the session.

The two dates are not required to be identical.

For a complete 365-day study program, approximately 365 Scripture Reading activities and approximately 365 Daily Sessions are expected.

---

# 20. Specification Status

Under Review — CP-014

Implementation must follow the finalized detection rules after the current session-detection code has been inspected.