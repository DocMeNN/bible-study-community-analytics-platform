# ADR-003 — Unified Presentation Scope Selection

## Status

**Accepted**

## Decision

The platform will provide a single unified Presentation Scope Selection workflow.

The user will first select one presentation period:

1. **Daily**
2. **Weekly**
3. **Monthly**
4. **First Half / Last Half of the Year**
5. **Yearly**

The selected presentation period will determine the available scope selector.

The platform must maintain **one active presentation scope at a time**.

The active presentation scope will be either:

```text
Daily Selection
        ↓
Daily Session
```

or:

```text
Weekly Selection
        ↓
Session Group
```

or:

```text
Monthly Selection
        ↓
Session Group
```

or:

```text
Half-Year Selection
        ↓
Session Group
```

or:

```text
Yearly Selection
        ↓
Session Group
```

The selected scope will be the single presentation context consumed by the dashboard, analytics views, reports, and other presentation-layer features.

---

# 1. Context

The platform stores and processes data at the level of the **Daily Session**.

The Presentation layer, however, supports displaying multiple Daily Sessions according to different user-selected time periods.

This creates two distinct concerns:

```text
Domain and Storage
        ↓
Daily Session
```

and:

```text
Presentation
        ↓
Daily
Weekly
Monthly
First Half / Last Half of Year
Yearly
```

The Presentation layer therefore needs a clear mechanism for allowing the user to choose how the imported SessionCollection should be viewed.

During implementation, a conflict was identified between:

```text
Daily Session Selector
```

and:

```text
Grouped Session Selector
```

Both could remain active simultaneously.

For example:

```text
Presentation Period
        ↓
Weekly
        ↓
Selected Weekly Group
```

while a separate Daily Session selector continued to hold:

```text
Selected Daily Session
```

The result was an inconsistent presentation state.

The user could select a Weekly group while the Overview and other components continued to use the independently selected Daily Session.

This created a conflict between:

```text
User's Visible Selection
```

and:

```text
Application's Active Analytical Scope
```

The architecture therefore requires a single, authoritative presentation selection model.

---

# 2. Problem Statement

The Presentation layer must avoid maintaining multiple independent active selections.

The following state is invalid:

```text
Selected Period:
    Weekly

Selected Weekly Group:
    Week 1

Selected Daily Session:
    January 3

Dashboard Scope:
    January 3
```

In this situation, the user believes the application is displaying:

```text
Week 1
```

while the application is actually calculating analytics for:

```text
January 3
```

This creates ambiguity and can produce misleading results.

The application must therefore ensure that:

> **The scope selected by the user is the same scope consumed by downstream presentation components.**

---

# 3. Core Architectural Principle

> **The Presentation layer must maintain one active presentation scope at a time.**

The presentation flow is:

```text
SessionCollection
        ↓
Presentation Period Selection
        ↓
Scope Selection
        ↓
Active Presentation Scope
        ↓
Dashboard
        ↓
Analytics
        ↓
Reports
```

The selected presentation period determines the type of scope available for selection.

```text
Daily
    ↓
Daily Session
```

```text
Weekly
    ↓
Weekly Session Group
```

```text
Monthly
    ↓
Monthly Session Group
```

```text
First Half / Last Half of Year
    ↓
Half-Year Session Group
```

```text
Yearly
    ↓
Yearly Session Group
```

Only one of these scopes may be active at any given time.

---

# 4. Presentation Period Options

The platform shall provide the following presentation period options.

## 4.1 Daily

```text
Daily
    ↓
Daily Session
```

The user selects one individual Daily Session.

Example:

```text
Presentation Period:
    Daily

Select Daily Session:
    January 15, 2023
```

The active presentation scope is:

```text
Daily Session
```

This is the most granular presentation level.

---

## 4.2 Weekly

```text
Weekly
    ↓
Weekly Session Group
```

The user selects one grouped weekly period.

Example:

```text
Presentation Period:
    Weekly

Select Week:
    January 8 – January 14, 2023
```

The active presentation scope is:

```text
Weekly Session Group
```

The group may contain:

```text
January 8
January 9
January 10
January 11
January 12
January 13
January 14
```

Each item remains an independent Daily Session.

The weekly presentation is only a Presentation-layer grouping.

---

## 4.3 Monthly

```text
Monthly
    ↓
Monthly Session Group
```

The user selects one calendar month.

Example:

```text
Presentation Period:
    Monthly

Select Month:
    January 2023
```

The active presentation scope is:

```text
Monthly Session Group
```

The group contains all detected Daily Sessions whose session dates fall within the selected calendar month.

Example:

```text
January 2023
├── January 1
├── January 3
├── January 5
├── January 8
├── January 10
└── ...
```

The exact number of Daily Sessions depends on the imported data.

---

## 4.4 First Half / Last Half of the Year

The platform shall support two half-year presentation periods:

```text
First Half of Year
```

and:

```text
Last Half of Year
```

The first half of a calendar year is:

```text
January 1
        ↓
June 30
```

The last half of a calendar year is:

```text
July 1
        ↓
December 31
```

The presentation options may therefore appear as:

```text
First Half of 2023
Last Half of 2023
```

Example:

```text
Presentation Period:
    First Half of Year

Select Period:
    January – June 2023
```

or:

```text
Presentation Period:
    Last Half of Year

Select Period:
    July – December 2023
```

The active presentation scope is:

```text
Half-Year Session Group
```

The underlying Daily Sessions remain unchanged.

---

## 4.5 Yearly

```text
Yearly
    ↓
Yearly Session Group
```

The user selects one calendar year.

Example:

```text
Presentation Period:
    Yearly

Select Year:
    2023
```

The active presentation scope contains all detected Daily Sessions within that calendar year.

Example:

```text
2023
├── January
├── February
├── March
├── ...
└── December
```

The Yearly presentation may provide high-level aggregated analytics while preserving access to the underlying Monthly, Weekly, and Daily Sessions.

---

# 5. Unified Selection Workflow

The user interface shall expose one unified selection workflow.

The conceptual flow is:

```text
┌──────────────────────────────────────┐
│ Select Presentation Period            │
│                                      │
│ Daily                                │
│ Weekly                               │
│ Monthly                              │
│ First Half / Last Half of Year       │
│ Yearly                               │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ Select Presentation Scope             │
│                                      │
│ Scope depends on selected period      │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ Active Presentation Scope             │
└──────────────────┬───────────────────┘
                   │
                   ▼
          Dashboard and Analytics
```

The second selector must dynamically reflect the first selection.

For example:

```text
Daily
    ↓
Select Daily Session
```

```text
Weekly
    ↓
Select Week
```

```text
Monthly
    ↓
Select Month
```

```text
First Half of Year
    ↓
Select First Half
```

```text
Last Half of Year
    ↓
Select Last Half
```

```text
Yearly
    ↓
Select Year
```

---

# 6. Single Active Scope Rule

At any given time, the Presentation layer shall have exactly one active presentation scope.

Conceptually:

```text
active_presentation_scope
```

The value may represent:

```text
Daily Session
```

or:

```text
Weekly Session Group
```

or:

```text
Monthly Session Group
```

or:

```text
Half-Year Session Group
```

or:

```text
Yearly Session Group
```

The application must not simultaneously treat multiple scopes as active.

Invalid:

```text
Active Daily Session
        +
Active Weekly Group
```

Invalid:

```text
Active Weekly Group
        +
Active Monthly Group
```

Valid:

```text
Active Presentation Scope
        ↓
One Selected Scope
```

---

# 7. Scope Transition Rules

When the user changes the presentation period, the previous scope selection must no longer control the application.

For example:

```text
Current:

Weekly
    ↓
Week 1
```

The user changes to:

```text
Monthly
```

The application must transition to:

```text
Monthly
    ↓
Select Month
```

The previous:

```text
Week 1
```

must no longer be the active presentation scope.

Similarly:

```text
Monthly
    ↓
January 2023
```

changed to:

```text
Daily
```

must result in:

```text
Daily
    ↓
Select Daily Session
```

The application must not continue using:

```text
January 2023
```

as the active scope.

The selected presentation period is therefore the authority that determines the active scope type.

---

# 8. Dashboard Integration

All presentation-layer dashboard components must consume the active presentation scope.

The flow shall be:

```text
Presentation Period
        ↓
Selected Scope
        ↓
Active Presentation Scope
        ↓
ViewModel
        ↓
Dashboard Component
```

The dashboard must not independently retrieve a different Daily Session or SessionGroup.

The following architecture is prohibited:

```text
User selects Weekly Group
        ↓
Weekly Group Selector

Overview
        ↓
context.current_session()
        ↓
Different Daily Session
```

The correct architecture is:

```text
User selects Weekly Group
        ↓
Active Presentation Scope
        ↓
Overview
        ↓
Weekly Group Analytics
```

For Daily:

```text
Daily Session
        ↓
Daily Analytics
```

For Weekly:

```text
Weekly Session Group
        ↓
Weekly Analytics
```

For Monthly:

```text
Monthly Session Group
        ↓
Monthly Analytics
```

For Half-Year:

```text
Half-Year Session Group
        ↓
Half-Year Analytics
```

For Yearly:

```text
Yearly Session Group
        ↓
Yearly Analytics
```

---

# 9. Relationship to the Daily Session Domain Model

This decision does not change the Domain model.

The atomic domain unit remains:

```text
Daily Session
```

The Presentation layer may group Daily Sessions into:

```text
Weekly Session Group
```

```text
Monthly Session Group
```

```text
Half-Year Session Group
```

```text
Yearly Session Group
```

The relationship is:

```text
Domain
    ↓
Daily Session
```

```text
Presentation
    ↓
Presentation Scope
    ├── Daily Session
    ├── Weekly Session Group
    ├── Monthly Session Group
    ├── Half-Year Session Group
    └── Yearly Session Group
```

The Presentation layer must not modify or redefine the Daily Session domain aggregate.

---

# 10. Relationship to ADR-002

This decision extends and operationalizes:

```text
ADR-002 — Multi-Level Session Presentation
```

ADR-002 establishes:

> **The platform stores Daily Sessions as the atomic domain unit while allowing the Presentation layer to group and display Sessions according to user-selected time periods.**

This ADR establishes how the user selects one of those presentation levels and how the selected level becomes the active scope for the application.

The relationship is therefore:

```text
ADR-002
    ↓
Defines available presentation grouping concepts

ADR-003
    ↓
Defines unified selection and active scope behavior
```

ADR-002 answers:

> How may Sessions be presented?

ADR-003 answers:

> How does the user select one presentation scope, and which scope controls the application?

---

# 11. Presentation State Model

The Presentation layer should conceptually maintain:

```text
Presentation State
```

containing:

```text
Selected Presentation Period
```

and:

```text
Selected Presentation Scope
```

Conceptually:

```text
PresentationState
├── period
└── scope
```

Examples:

```text
PresentationState
├── period: DAILY
└── scope: Daily Session
```

```text
PresentationState
├── period: WEEKLY
└── scope: Weekly Session Group
```

```text
PresentationState
├── period: MONTHLY
└── scope: Monthly Session Group
```

```text
PresentationState
├── period: FIRST_HALF
└── scope: First-Half Session Group
```

```text
PresentationState
├── period: LAST_HALF
└── scope: Last-Half Session Group
```

```text
PresentationState
├── period: YEARLY
└── scope: Yearly Session Group
```

The active scope must always be consistent with the selected period.

Invalid:

```text
period = WEEKLY
scope = Daily Session
```

Invalid:

```text
period = MONTHLY
scope = Weekly Session Group
```

Valid:

```text
period = WEEKLY
scope = Weekly Session Group
```

---

# 12. Selection Consistency Invariant

The following invariant shall apply:

> **The active presentation scope must always correspond to the selected presentation period.**

Formally:

```text
Daily
    → Daily Session

Weekly
    → Weekly Session Group

Monthly
    → Monthly Session Group

First Half
    → First-Half Session Group

Last Half
    → Last-Half Session Group

Yearly
    → Yearly Session Group
```

No downstream component may bypass this active scope and independently select another presentation scope.

---

# 13. Navigation Model

The unified presentation scope provides the entry point for navigation.

The navigation flow may be:

```text
Presentation Period
        ↓
Presentation Scope
        ↓
Scope Overview
        ↓
Contained Daily Sessions
        ↓
Individual Daily Session
```

For example:

```text
Weekly
    ↓
January 8 – January 14
    ↓
Weekly Overview
    ↓
Daily Sessions
    ↓
January 10
    ↓
Daily Session Details
```

For Monthly:

```text
Monthly
    ↓
January 2023
    ↓
Monthly Overview
    ↓
Weekly or Daily Breakdown
    ↓
Individual Daily Session
```

For Yearly:

```text
Yearly
    ↓
2023
    ↓
Yearly Overview
    ↓
Monthly Breakdown
    ↓
Weekly Breakdown
    ↓
Daily Sessions
```

Navigation may move from a broad presentation scope to a more detailed scope.

However, only the currently selected scope is the active analytical scope at any given time.

---

# 14. Selection UI Principle

The interface must provide:

```text
One Presentation Period Selector
```

followed by:

```text
One Contextual Scope Selector
```

Example:

```text
┌──────────────────────────────┐
│ Presentation Period          │
│ [ Weekly              ▼ ]    │
└──────────────────────────────┘

┌──────────────────────────────┐
│ Select Week                  │
│ [ Jan 8 – Jan 14, 2023 ▼ ]   │
└──────────────────────────────┘
```

When the user changes the period:

```text
[ Monthly ▼ ]
```

the second selector changes to:

```text
┌──────────────────────────────┐
│ Select Month                 │
│ [ January 2023         ▼ ]   │
└──────────────────────────────┘
```

The application must not display unrelated selectors simultaneously.

Therefore, the following design is prohibited:

```text
Select Daily Session
        +
Select Weekly Group
```

when only one presentation scope can be active.

---

# 15. Implementation Boundary

The implementation belongs to the Presentation layer.

The Presentation layer is responsible for:

* Rendering the presentation period selector.
* Rendering the contextual scope selector.
* Managing the active presentation scope.
* Synchronizing Streamlit state.
* Providing the active scope to ViewModels and presentation components.

The Application layer is responsible for:

* Executing application use cases.
* Coordinating services.
* Providing analytical results.

The Domain layer is responsible for:

* Daily Session rules.
* Attendance rules.
* Activity rules.
* Domain analytics.

The Infrastructure layer is responsible for:

* Data loading.
* Parsing.
* External integrations.
* Persistence and technical services.

The dependency flow remains:

```text
Presentation
      ↓
Application
      ↓
Domain
      ↑
Infrastructure
```

The Presentation layer must not move grouping logic into the Domain layer.

---

# 16. Required Implementation Direction

The Presentation layer should evolve toward a unified active-scope workflow.

Conceptually:

```text
SessionCollection
        ↓
Presentation Period Selector
        ↓
Scope Selector
        ↓
Active Presentation Scope
        ↓
ViewModels
        ↓
Dashboard
```

The existing independent Daily Session selector and grouped-period selector must not remain as competing sources of truth.

The implementation must establish:

```text
One Period
        +
One Scope
        =
One Active Presentation Context
```

---

# 17. Final Decision

The platform officially adopts the following unified presentation selection model:

```text
1. DAILY
      ↓
   Daily Session
```

```text
2. WEEKLY
      ↓
   Weekly Session Group
```

```text
3. MONTHLY
      ↓
   Monthly Session Group
```

```text
4. FIRST HALF / LAST HALF OF YEAR
      ↓
   Half-Year Session Group
```

```text
5. YEARLY
      ↓
   Yearly Session Group
```

The platform shall maintain:

```text
One Selected Presentation Period
```

and:

```text
One Active Presentation Scope
```

The selected scope shall be the authoritative scope used by the Presentation layer.

The central decision is:

> **One presentation period. One contextual scope selector. One active presentation scope. One source of truth for the dashboard.**

The architecture therefore becomes:

```text
SessionCollection
        ↓
Presentation Period
        ↓
Contextual Scope Selection
        ↓
Active Presentation Scope
        ↓
Dashboard
        ↓
Analytics
        ↓
Reports
```

The domain remains centered on:

```text
Daily Session
```

The Presentation layer determines how those Daily Sessions are navigated and consumed.

> **The Domain preserves the atomic truth. The Presentation layer determines the user's active view of that truth.**
