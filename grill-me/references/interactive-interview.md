# Interactive Interview Guidelines & Alignment Axes 📋

A guide for AI coding agents to structure deep technical questionnaires when executing the `/grill-me` protocol.

---

## 1. Five Fundamental Axes of Any Technical Task

When constructing native form modals (`ask_question` / `AskUserQuestion`), ensure the following axes are addressed:

1. **Scope & Delivery Boundaries**:
   - What is the minimum viable deliverable for this task?
   - Which files, endpoints, or modules must NOT be modified?
2. **Architecture & Data Contracts**:
   - What architectural pattern should be followed (Clean Architecture, MVC, Event-driven)?
   - How should data payloads flow (REST, GraphQL, gRPC, WebSockets)?
3. **State Management & Dependencies**:
   - Which existing libraries or utilities in the codebase should be reused?
   - What persistence or caching mechanism should be employed?
4. **Interface & User Experience (if applicable)**:
   - What design system tokens or CSS conventions apply?
   - How should loading spinners, empty states, and network errors be rendered?
5. **Testing & Validation Strategy**:
   - Which test levels are mandatory (unit, integration, e2e)?
   - Are there specific coverage thresholds or CI pipelines that must pass?

---

## 2. Best Practices for Formulating Options

- **Be Concrete**: Avoid ambiguous questions like *"What database do you want?"*. Prefer: *"Which database engine should be used for the telemetry audit store?"*.
- **Ground the Recommendation**: In the first `(Recommended)` option, summarize the technical rationale (e.g., `(Recommended) Local SQLite in WAL mode — zero external infrastructure, sub-millisecond query latency`).
- **Respect User Selection**: When the user picks a non-recommended option, accept the architectural decision without arguing and execute accordingly.
