# ADR-002 Multi-Level Session Presentation

## Status

**Accepted**

## Decision

The platform will maintain **Daily Session** as the atomic domain and storage unit while allowing the Presentation layer to group and display sessions according to user-selected time periods.

The default presentation grouping will be **Week**.

---

# 1. Context

The platform processes WhatsApp exports containing the complete history of a Bible study community.

The underlying data is naturally divided into individual study sessions. However, displaying every session individually becomes increasingly difficult to navigate as the dataset grows.

For example:

```text
Daily View

Jan 1
Jan 2
Jan 3
Jan 4
Jan 5
...
365 sessions per year
```

This is technically accurate but increasingly difficult for users to browse and understand.

The way data is stored does not necessarily need to be the same as the way users consume it.

Therefore, the architecture must distinguish between:

```text
Storage Unit
    ↓
Daily Session

Presentation Unit
    ↓
Weekly Study Period
```

These are deliberately different concepts.

---

# 2. Core Architectural Principle

> **The domain stores individual Daily Sessions. The Presentation layer groups Daily Sessions for human consumption.**

The domain model must remain stable and independent of presentation preferences.

```text
Domain
    ↓
Daily Session
    ↓
Daily Session
    ↓
Daily Session
    ↓
Daily Session
```

The Presentation layer may aggregate these sessions into different navigation views:

```text
Year
    ↓
Month
    ↓
Week
    ↓
Daily Session
```

Each higher level is an aggregation of the level below it.

---

# 3. Domain Storage Unit

The atomic unit of the platform remains:

## Daily Session

A Daily Session represents one detected study period based on the platform's session detection rules.

A Daily Session contains:

* One Scripture Reading boundary.
* One day's activities.
* One day's participation.
* One day's attendance analytics.
* One day's activity analytics.
* One day's AI summary.
* One session date.
* One collection of messages and derived events.

The Daily Session is the fundamental unit for:

* Domain calculations.
* Attendance analytics.
* Activity analytics.
* Session-level AI analysis.
* Session persistence.
* Session-level reporting.

This decision does not change the domain model.

```text
Daily Session
├── Session Date
├── Messages
├── Attendance Events
├── Activity Events
├── Participants
├── Attendance Analytics
├── Activity Analytics
└── AI Session Intelligence
```

---

# 4. Presentation Unit

The Presentation layer must not assume that the user wants to navigate every Daily Session individually.

Instead, the platform should provide configurable grouping.

The default presentation view is:

```text
Weekly Study Period
```

For example:

```text
Week 1
January 1 – January 7

7 Sessions
Average Participants: 18
DONE Acknowledgements: 265
Activity Events: 78

Open ▶
```

The user may then expand the weekly period to access its individual Daily Sessions.

```text
Week 1
├── January 1 — Daily Session
├── January 2 — Daily Session
├── January 3 — Daily Session
├── January 4 — Daily Session
├── January 5 — Daily Session
├── January 6 — Daily Session
└── January 7 — Daily Session
```

---

# 5. Default Presentation Hierarchy

The default hierarchy is:

```text
Year
    │
    ▼
Month
    │
    ▼
Week
    │
    ▼
Daily Session
```

The hierarchy is a navigation and aggregation structure.

It does not alter the underlying SessionCollection.

The underlying data remains:

```text
SessionCollection
    ├── Daily Session
    ├── Daily Session
    ├── Daily Session
    ├── Daily Session
    └── ...
```

The Presentation layer creates a view over that collection.

---

# 6. Configurable Session Grouping

The user should be able to select how sessions are grouped.

## Group Sessions By

```text
( ) Day
(✓) Week
( ) Month
( ) Quarter
( ) Year
```

The same underlying SessionCollection can therefore be presented in different ways.

```text
Daily Grouping

January 1
January 2
January 3
January 4
...
```

```text
Weekly Grouping

Week 1
Week 2
Week 3
Week 4
...
```

```text
Monthly Grouping

January 2023
February 2023
March 2023
...
```

```text
Quarterly Grouping

Q1 2023
Q2 2023
Q3 2023
Q4 2023
```

```text
Yearly Grouping

2023
2024
2025
```

The data does not change.

Only the presentation grouping changes.

---

# 7. Default Week Definition

The default study week will end on:

```text
Saturday
```

Therefore, the default study period is:

```text
Sunday → Saturday
```

Example:

```text
Week 18

Sunday, May 3
        ↓
Saturday, May 9
```

Another example:

```text
Week 1

Sunday, January 4
        ↓
Saturday, January 10
```

The platform should compute these boundaries automatically.

The user should not need to manually assign sessions to weeks.

---

# 8. Configurable Study Calendar

The study calendar must be configurable.

The Settings layer should eventually provide:

## Study Calendar

### Week Ends On

```text
( ) Saturday
( ) Sunday
( ) Friday
( ) Custom
```

This allows the platform to support different ministry and organizational rhythms.

Examples:

```text
Sunday → Saturday
```

For a ministry that follows the traditional weekly cycle.

```text
Monday → Sunday
```

For a conventional business or operational week.

```text
Monday → Friday
```

For a weekday-only study program.

The analytics layer must not depend on the chosen week boundary.

Only the grouping and presentation logic changes.

---

# 9. Aggregation Rules

Each presentation grouping is an aggregation of the underlying Daily Sessions.

## Day

```text
1 Daily Session
```

The displayed values come directly from the Daily Session.

---

## Week

```text
Daily Session
    +
Daily Session
    +
Daily Session
    +
Daily Session
    +
Daily Session
    +
Daily Session
    +
Daily Session
    ↓
Weekly Study Period
```

Possible weekly metrics include:

* Number of Daily Sessions.
* Total attendance events.
* Average participants.
* Maximum participants.
* Minimum participants.
* Total DONE acknowledgements.
* Total activity events.
* Unique participants across the period.
* Attendance trend.
* Activity trend.
* AI-generated weekly insights.

---

## Month

```text
Week
    +
Week
    +
Week
    +
Week
    ↓
Monthly Study Period
```

The same principle applies.

---

## Quarter

```text
Month
    +
Month
    +
Month
    ↓
Quarterly Study Period
```

---

## Year

```text
Quarter
    +
Quarter
    +
Quarter
    +
Quarter
    ↓
Yearly Study Period
```

---

# 10. Navigation Model

The user should be able to navigate from broad periods to individual sessions.

Example:

```text
Year: 2023
    │
    ▼
Month: January
    │
    ▼
Week: Week 1
    │
    ▼
Daily Session: January 1
```

The interface should support:

```text
Overview
    ↓
Grouped Period
    ↓
Daily Sessions
    ↓
Individual Session Details
```

For example:

```text
Week 1
January 1 – January 7

7 Sessions
Average Participants: 18
Total DONE Events: 265
Total Activity Events: 78

[Open Week]
```

Then:

```text
Daily Sessions

01-01-2023
03-01-2023
04-01-2023
05-01-2023
07-01-2023
08-01-2023
09-01-2023
```

Selecting a Daily Session opens the existing session-level analytics.

---

# 11. Why Weekly Presentation Is the Default

The weekly view is the preferred default because it balances detail and navigability.

For a single year:

```text
Daily View

365 sessions
```

Compared with:

```text
Weekly View

Approximately 52 weeks
```

And:

```text
Monthly View

12 months
```

For five years:

```text
Daily View

Approximately 1,825 sessions
```

```text
Weekly View

Approximately 260 weeks
```

```text
Monthly View

60 months
```

The weekly view provides a significantly more manageable navigation experience while retaining access to the underlying Daily Sessions.

---

# 12. Architectural Separation

This decision establishes the following separation:

```text
┌────────────────────────────────────────────┐
│              DOMAIN LAYER                  │
│                                            │
│  Daily Session                             │
│  Attendance                                │
│  Activity                                  │
│  Analytics                                 │
│  AI Session Intelligence                   │
│                                            │
│  Storage Unit: DAILY SESSION               │
└────────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────┐
│          PRESENTATION LAYER                │
│                                            │
│  Day                                       │
│  Week                                      │
│  Month                                     │
│  Quarter                                   │
│  Year                                      │
│                                            │
│  Presentation Unit: CONFIGURABLE GROUPING  │
└────────────────────────────────────────────┘
```

The Presentation layer must not modify the domain's atomic unit.

The Domain layer must not know whether the user is viewing:

* A day.
* A week.
* A month.
* A quarter.
* A year.

---

# 13. Future Implementation Direction

The future Presentation architecture should introduce a dedicated grouping workflow.

Conceptually:

```text
SessionCollection
        │
        ▼
Session Grouping Configuration
        │
        ▼
Grouping Strategy
        │
        ├── Day
        ├── Week
        ├── Month
        ├── Quarter
        └── Year
        │
        ▼
Grouped Session View
```

A future implementation may introduce concepts such as:

```text
SessionGrouping
```

or:

```text
SessionPeriod
```

or:

```text
SessionGroupingViewModel
```

The exact implementation should be determined during a future architecture checkpoint.

The important architectural decision is already established:

> **Grouping is a Presentation concern and must not be embedded into the Daily Session domain model.**

---

# 14. Current Implementation Status

The current platform has successfully implemented the multi-session foundation.

The current state is:

```text
SessionCollection
    ├── Daily Session 1
    ├── Daily Session 2
    ├── Daily Session 3
    ├── Daily Session 4
    └── ...
```

The Home page currently displays the imported sessions as a chronological session timeline.

The next evolution is to provide configurable grouping and navigation over the same SessionCollection.

The first implementation target should be:

```text
Default Grouping:
Week

Underlying Storage:
Daily Session

Navigation:
Week → Daily Session
```

---

# 15. Final Decision

The architecture officially adopts the following model:

```text
STORAGE

Daily Session
```

```text
DEFAULT PRESENTATION

Weekly Study Period
```

```text
AVAILABLE PRESENTATION GROUPINGS

Day
Week
Month
Quarter
Year
```

```text
DEFAULT STUDY WEEK

Sunday → Saturday
```

```text
CONFIGURABLE WEEK END

Saturday
Sunday
Friday
Custom
```

The central architectural principle is:

> **Store at the Daily Session level. Present at the level most useful to the user.**

Or, more concisely:

> **The data model serves the truth. The presentation model serves the user.**

This decision is now part of the platform's architectural reference baseline and should guide all future session navigation, aggregation, dashboard, reporting, and calendar-related implementation.
