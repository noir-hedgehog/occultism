# astrology_compatibility_guard

## Purpose

Guard synastry, compatibility and relationship-astrology requests before any chart interpretation. This tool keeps astrology relationship work symbolic, consent-aware and non-deterministic.

## Input

```json
{
  "request_text": "我和伴侣有外部合盘字段，想看沟通模式和边界",
  "all_subjects_self_or_consented": true
}
```

Optional consent hints:

- `all_subjects_self_or_consented`
- `other_subject_consent`
- `relationship_is_self_reflection_only`

## Output

The tool returns:

- relationship intent
- consent state
- risk flags
- whether compatibility interpretation can continue
- a safe reframed question
- warnings, limits and next workflow steps

## Boundaries

- Do not decide whether people are soulmates, doomed, destined to separate, or certain to reunite.
- Do not infer a third party's real thoughts, feelings, sexuality, secrets or character without consent.
- Do not use astrology to coerce, control, stalk, retaliate or force reconciliation.
- Use chart fields only after source and consent are recorded.
