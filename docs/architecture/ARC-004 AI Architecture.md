# Online Bible Study Attendance and Participation Analytics Platform

# ARC-004

# AI Architecture

---

## Document Information

| Property | Value |
|----------|-------|
| Document ID | ARC-004 |
| Title | AI Architecture |
| Version | 1.0 |
| Status | Draft |
| Classification | Public |
| Owner | TechAndMe |
| Author | TechAndMe |
| Reviewer | Chief Architect |
| Approver | Chief Architect |
| Effective Date | July 2026 |
| Last Updated | July 2026 |

---

> **Building Better Software.**
>
> **Building Better Engineers.**

---

# Table of Contents

1. Preamble
2. Purpose
3. Scope
4. Role of AI in the Platform
5. AI Architectural Principles
6. AI Architecture Overview
7. AI Provider Abstraction
8. AI Provider Implementations
9. Related Documents
10. Revision History
11. Closing Reflection

---

# Preamble

Artificial Intelligence provides an additional layer of intelligence within the Online Bible Study Attendance and Participation Analytics Platform.

The platform uses AI to assist with the interpretation, summarisation, and presentation of analytical information.

AI does not replace the platform's deterministic analytics.

Instead, AI operates as an intelligence layer that builds upon validated domain and analytical results.

This distinction is fundamental.

The platform determines analytical facts through deterministic processing.

AI may then assist users in understanding those facts through natural-language summaries, insights, and explanations.

The AI architecture is therefore designed to be:

- modular;
- provider-independent;
- replaceable;
- testable;
- locally executable where practical;
- extensible for future capabilities.

---

# 1. Purpose

The purpose of this document is to define the architecture of Artificial Intelligence within the platform.

It establishes:

- the role of AI;
- provider abstraction;
- AI provider implementations;
- AI task organisation;
- prompt management;
- AI service coordination;
- provider selection;
- error handling;
- AI integration boundaries.

This document serves as the authoritative architectural reference for AI-assisted capabilities.

---

# 2. Scope

This document covers the AI architecture of the platform.

It includes:

- AI provider abstraction;
- provider implementations;
- provider selection;
- AI tasks;
- prompt management;
- AI service coordination;
- response handling;
- AI error handling;
- AI presentation integration.

It does not define:

- core business rules;
- deterministic analytics;
- user interface design;
- deployment infrastructure;
- provider-specific operational infrastructure in detail.

Those concerns are documented separately.

---

# 3. Role of AI in the Platform

AI provides interpretive and generative capabilities that complement the platform's deterministic analytical engine.

AI may assist with:

- session summaries;
- analytical explanations;
- participation insights;
- report narratives;
- trend interpretation;
- natural-language responses.

AI shall not be treated as the authoritative source of analytical truth.

The platform's deterministic analytical systems remain responsible for calculating:

- attendance;
- participation;
- activity;
- recognition;
- analytical metrics.

AI may interpret these results but shall not silently replace the underlying calculations.

---

# 4. AI Architectural Principles

The AI architecture follows the following principles.

## Provider Independence

The application should not depend directly on a specific AI provider.

---

## Replaceability

An AI provider should be replaceable without requiring major changes to application workflows.

---

## Deterministic Analytics First

AI should complement validated analytical results rather than replace them.

---

## Local-First Capability

Where practical, local AI execution should be supported to improve:

- privacy;
- availability;
- cost control;
- experimentation.

---

## Explicit AI Tasks

AI capabilities should be represented as clearly defined tasks rather than scattered prompts throughout the application.

---

## Controlled Integration

AI access should occur through defined architectural boundaries.

---

## Graceful Failure

The platform should remain useful when AI services are unavailable.

---

# 5. AI Architecture Overview

The high-level AI architecture is represented below.

```text
Presentation Layer
        │
        ▼
AI ViewModel
        │
        ▼
AI Application Service
        │
        ▼
AI Task
        │
        ▼
AI Provider Interface
        │
        ├───────────────┐
        ▼               ▼
   OpenAI          Gemini
        │
        └───────────────┐
                        ▼
                      Ollama
```

The application interacts with an abstract AI provider contract.

Provider-specific implementations remain isolated behind that abstraction.

---

# 6. AI Provider Abstraction

The AI Provider abstraction defines the common contract used by all AI providers.

The abstraction allows the application to request AI operations without knowing which provider performs the work.

A provider may be:

- cloud-based;
- locally hosted;
- remotely hosted;
- replaced in the future.

The application should interact with the provider interface rather than directly with provider-specific SDKs.

---

# 7. AI Provider Implementations

The platform supports multiple AI provider implementations.

Current providers include:

- OpenAI;
- Google Gemini;
- Ollama.

Each provider implements the common AI Provider contract.

This architecture enables the platform to select the appropriate provider according to:

- configuration;
- availability;
- user preference;
- privacy requirements;
- operational requirements.

---

# 8. AI Provider Architecture

The AI Provider Architecture separates application-level AI requirements from provider-specific implementations.

The application interacts with a common provider contract.

```text
AI Application Service
        │
        ▼
   AI Provider
   Interface
        │
        ├───────────────┬───────────────┐
        ▼               ▼               ▼
 OpenAI Provider   Gemini Provider   Ollama Provider
```

Each provider is responsible for translating the common application request into the format required by its underlying AI technology.

The Application Layer should not contain provider-specific implementation details.

---

# 9. AI Provider Interface

The AI Provider Interface defines the common contract implemented by all AI providers.

The interface provides a consistent mechanism for:

- sending prompts;
- receiving responses;
- handling provider errors;
- reporting provider availability.

The interface allows the application to remain independent of:

- provider SDKs;
- API request formats;
- authentication mechanisms;
- local model execution details;
- provider-specific response formats.

---

# 10. AI Provider Factory

The AI Provider Factory is responsible for creating the appropriate provider implementation.

The factory receives a configured provider selection and returns the corresponding implementation.

```text
Provider Configuration
        │
        ▼
 AI Provider Factory
        │
        ├───────────────┬───────────────┐
        ▼               ▼               ▼
 OpenAI Provider   Gemini Provider   Ollama Provider
```

The factory centralises provider selection.

This prevents provider selection logic from being duplicated throughout the application.

Provider selection may be determined by:

- application configuration;
- user preference;
- environment settings;
- operational requirements.

---

# 11. Supported AI Providers

## 11.1 OpenAI Provider

The OpenAI Provider connects the platform to OpenAI-compatible cloud AI services.

Its responsibilities include:

- managing provider-specific requests;
- handling authentication;
- translating application prompts;
- translating provider responses;
- handling provider-specific errors.

The provider implementation remains behind the common AI Provider interface.

---

## 11.2 Gemini Provider

The Gemini Provider connects the platform to Google Gemini AI services.

Its responsibilities include:

- managing provider-specific requests;
- handling authentication;
- translating application prompts;
- translating provider responses;
- handling provider-specific errors.

The application remains independent of the Gemini implementation.

---

## 11.3 Ollama Provider

The Ollama Provider enables local AI model execution.

This supports a local-first architecture where AI processing may occur on the user's own machine.

Local execution provides potential benefits including:

- improved data privacy;
- reduced external dependency;
- offline-capable AI workflows;
- reduced API costs;
- local experimentation.

The Ollama Provider communicates with the locally running Ollama service while exposing the same common AI contract as other providers.

---

# 12. AI Task Architecture

AI capabilities are organised into explicit application-level tasks.

An AI task represents a defined AI-assisted capability.

Examples include:

- Session Summary;
- Scripture Summary;
- Participation Insight;
- Report Narrative;
- Engagement Interpretation.

The general execution model is:

```text
Application Request
        │
        ▼
      AI Task
        │
        ▼
 Prompt Construction
        │
        ▼
 AI Provider
        │
        ▼
 AI Response
        │
        ▼
 Response Processing
```

AI tasks should remain focused on a specific purpose.

A task should not become a general-purpose container for unrelated AI operations.

---

# 13. Prompt Management

Prompts should be treated as application assets rather than scattered strings embedded throughout user interface code.

Prompt construction should be:

- explicit;
- maintainable;
- testable;
- versionable.

A prompt may contain:

- system instructions;
- task instructions;
- analytical context;
- structured data;
- output requirements.

The prompt should provide sufficient context for the AI task while avoiding unnecessary exposure of unrelated data.

---

# 14. AI Context Preparation

Before an AI task is executed, the Application Layer should prepare the relevant context.

```text
Domain Data
     │
     ▼
Analytics Results
     │
     ▼
Context Preparation
     │
     ▼
Prompt Construction
     │
     ▼
AI Provider
```

The AI should receive validated and relevant information.

AI tasks should not independently reconstruct authoritative analytics when validated analytical results are already available.

---

# 15. AI Response Processing

AI responses should pass through an application-level processing stage before presentation.

The processing stage may:

- validate the response;
- normalise the output;
- detect empty responses;
- handle provider errors;
- prepare the result for presentation.

The Presentation Layer should not be responsible for interpreting provider-specific response formats.

---

# 16. AI Service Coordination

The AI Service coordinates the execution of AI-assisted application capabilities.

Its responsibilities include:

- receiving AI task requests;
- preparing task context;
- selecting the configured provider;
- executing the AI task;
- processing the response;
- coordinating error handling.

The AI Service acts as an application-level coordinator.

It does not contain provider-specific implementation details.

---

# 17. AI Execution Flow

The complete AI execution flow is represented below.

```text
User Request
      │
      ▼
Presentation Layer
      │
      ▼
AI ViewModel
      │
      ▼
AI Application Service
      │
      ▼
AI Task
      │
      ▼
Context Preparation
      │
      ▼
Prompt Construction
      │
      ▼
AI Provider Factory
      │
      ▼
Selected AI Provider
      │
      ▼
AI Model
      │
      ▼
Provider Response
      │
      ▼
Response Processing
      │
      ▼
AI Result
      │
      ▼
Presentation Layer
```

Each stage has a defined responsibility.

---

# 18. AI Presentation Integration

The Presentation Layer provides the user-facing interface for AI capabilities.

AI presentation components may include:

- AI action buttons;
- loading indicators;
- provider selectors;
- provider status indicators;
- AI result displays;
- error messages;
- summary cards.

The Presentation Layer should:

- initiate AI requests;
- display execution status;
- display results;
- communicate errors to the user.

The Presentation Layer should not:

- construct provider-specific API requests;
- contain AI business rules;
- directly call AI SDKs;
- contain prompt orchestration logic.

---

# 19. Provider Selection

The platform may support provider selection through configuration or user preferences.

The provider selection process is:

```text
Provider Selection
        │
        ▼
Configuration
        │
        ▼
AI Provider Factory
        │
        ▼
Provider Instance
```

The selected provider should be transparent to the application workflow.

The same AI task should be capable of executing through different providers where compatible.

---

# 20. Local AI Architecture

Local AI execution is an important capability of the platform.

The local AI architecture is represented below.

```text
Platform
   │
   ▼
Ollama Provider
   │
   ▼
Local Ollama Service
   │
   ▼
Local AI Model
```

Local AI execution may provide:

- improved privacy;
- reduced dependence on external services;
- reduced API costs;
- offline-capable workflows;
- greater control over model selection.

The platform should treat local AI as a first-class provider rather than a special-case implementation.

---

# 21. AI Error Handling

AI operations may fail for several reasons.

Potential failure categories include:

- provider unavailable;
- invalid configuration;
- authentication failure;
- network failure;
- model unavailable;
- timeout;
- malformed response;
- empty response;
- rate limiting.

The AI architecture should translate provider-specific failures into application-level errors where appropriate.

```text
Provider Error
      │
      ▼
Provider Error Handling
      │
      ▼
Application-Level Error
      │
      ▼
Presentation Feedback
```

The platform should fail gracefully when AI is unavailable.

AI failure should not compromise the availability of deterministic analytics.

---

# 22. AI Availability

The platform should remain useful even when AI services are unavailable.

The following capabilities should remain operational independently of AI:

- data import;
- session detection;
- attendance analysis;
- activity analysis;
- participation analytics;
- recognition;
- deterministic reporting.

AI should be treated as an enhancement layer rather than a mandatory dependency for core analytical functionality.

---

# 23. AI Data Boundaries

AI tasks should receive only the information necessary to perform their assigned function.

Data boundaries should be defined according to:

- task requirements;
- privacy considerations;
- data minimisation principles;
- provider capabilities.

The platform should avoid unnecessarily transmitting:

- unrelated participant data;
- unnecessary personal information;
- raw data when an aggregated analytical result is sufficient.

Where local execution is available, it may be preferred for sensitive analytical contexts.

---

# 24. AI Result Trust Model

AI-generated results should be treated as interpretive outputs.

The platform should distinguish between:

```text
Deterministic Analytics
        │
        ▼
Authoritative Facts
        │
        ▼
AI Interpretation
        │
        ▼
Natural-Language Insight
```

AI-generated text should not silently alter the underlying analytical results.

Where appropriate, AI-generated insights should be presented as:

- summaries;
- interpretations;
- explanations;
- suggestions.

The original analytical results remain the authoritative source.

---

# 25. AI Security and Privacy

AI integrations shall be designed with appropriate consideration for data security and privacy.

The platform should:

- minimise unnecessary data transmission;
- avoid exposing sensitive data unnecessarily;
- protect provider credentials;
- avoid storing secrets in source code;
- use environment-based configuration where appropriate;
- distinguish local and external AI execution.

Provider credentials and API keys shall not be committed to the repository.

---

# 26. AI Testing Strategy

AI architecture requires testing at multiple levels.

## Provider Interface Testing

The common provider contract should be tested to ensure consistent behaviour across implementations.

---

## Provider Implementation Testing

Individual providers should be tested for:

- successful execution;
- configuration failures;
- unavailable services;
- malformed responses;
- timeout behaviour.

---

## AI Task Testing

AI tasks should be tested for:

- correct context preparation;
- correct prompt construction;
- response processing;
- error handling.

---

## Integration Testing

Provider integrations should be tested separately from deterministic domain analytics.

The failure of an AI provider should not invalidate the core analytical system.

---

# 27. AI Observability

AI operations should provide sufficient information for troubleshooting and operational monitoring.

Where appropriate, the platform may record:

- selected provider;
- task executed;
- execution status;
- execution duration;
- failure category.

Sensitive prompt content and personally identifiable information should not be logged unnecessarily.

---

# 28. AI Extensibility

The AI architecture is designed to support future expansion.

Potential future capabilities include:

- additional AI providers;
- additional local models;
- model selection;
- structured AI outputs;
- AI-assisted report generation;
- conversational analytics;
- retrieval-augmented generation;
- specialised analytical agents.

New AI capabilities should be introduced through the existing abstraction and task architecture wherever practical.

---

# 29. Architectural Constraints

The following constraints govern AI integration.

- AI providers shall remain behind an abstraction.
- Provider-specific SDKs shall not leak into the Presentation Layer.
- AI shall not replace authoritative deterministic analytics.
- AI tasks shall have clearly defined responsibilities.
- AI failures shall be handled gracefully.
- Provider credentials shall not be stored in source code.
- AI-generated results shall be distinguished from deterministic facts.
- AI integrations should remain replaceable.

These constraints protect the maintainability and reliability of the AI architecture.

---

# 30. Architectural Governance

Significant changes to AI architecture should be reviewed before implementation.

Examples include:

- adding a new provider;
- changing the provider abstraction;
- changing the AI task execution model;
- introducing external data retrieval;
- introducing autonomous AI agents;
- changing privacy boundaries;
- changing the relationship between AI and deterministic analytics.

Architectural changes should be documented through the appropriate Engineering Decision Record or Architecture Decision Record.

---

# 31. Related Documents

## Architecture Library

- ARC-001 System Architecture
- ARC-002 Application Architecture
- ARC-003 Domain Architecture
- ARC-005 Reporting Architecture
- ARC-006 Presentation Architecture
- ARC-007 Infrastructure Architecture
- ARC-008 Data Architecture
- ARC-009 Security Architecture

## Business Documentation

- BUS-003 Requirements
- BUS-006 Analytics Definitions

## Specifications

- SPEC-004 Analytics Engine
- SPEC-006 AI Summary Engine
- SPEC-007 Reporting Specification

## TechAndMe Playbook

- TMP-003 Engineering Principles
- TMP-006 Architecture Review Process
- TMP-007 Checkpoint Framework
- TMP-008 Engineering Reference System
- TMP-115 AI Engineering Guidelines
- TMP-127 AI-Assisted Software Engineering Framework

---

# 32. Revision History

| Version | Date | Description | Author |
|----------|------|-------------|--------|
| 1.0 | July 2026 | Initial AI Architecture | TechAndMe |

---

# 33. Closing Reflection

Artificial Intelligence provides an important extension to the analytical capabilities of the platform.

However, the architecture deliberately places AI in its proper position.

The platform's core analytical truth comes from deterministic domain and analytics logic.

AI adds interpretation.

AI adds explanation.

AI adds natural-language understanding.

AI adds a new way for users to interact with analytical knowledge.

By separating these responsibilities, the platform can benefit from the power of Artificial Intelligence without becoming dependent upon a particular provider, model, or technology.

The AI architecture therefore reflects a central engineering principle:

> **Use intelligence to enhance understanding, but preserve architecture to protect truth.**

As the field of Artificial Intelligence continues to evolve, the platform can adopt new providers, models, and capabilities while preserving its architectural foundations.

---

**Online Bible Study Attendance and Participation Analytics Platform**

**Architecture Library**

**Building Better Software.**

**Building Better Engineers.**

*"One step at a time. All the way."*

© TechAndMe