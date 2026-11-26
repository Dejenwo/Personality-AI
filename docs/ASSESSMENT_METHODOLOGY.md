# Assessment methodology

## Scoring algorithm `personalitydna.scoring.v1`

1. Validate item ids and integer Likert values in `[min, max]`.
2. Reverse-key: `score = (max + min) - raw` for `-` items.
3. Trait raw sum = sum of keyed item scores for answered items.
4. Trait mean = raw sum / answered count.
5. Display 0–100 = min-max of the trait’s possible raw range. **Not a percentile.**
6. Emotional Stability is scored as IPIP Factor IV. Negative Emotionality is displayed as the inverse mean `6 - ES_mean`.
7. Completion rules are per instrument (`min_answered_ratio`, `max_missing`).
8. `response_hash` = SHA-256 of canonical JSON `{slug, version, responses}`.

AI systems must not call this algorithm to invent scores.

## Instruments

| Slug | Origin | Validation status |
| --- | --- | --- |
| quick-discovery | Mini-IPIP item selection (Donnellan et al., 2006); IPIP wording | research_backed_short_form |
| big-five, comprehensive, advanced | IPIP-50 Big-Five Factor Markers | research_backed_public_domain |
| others | Original PersonalityDNA inventories | original_unvalidated |

See `assessment-content/instruments/` and `docs/ASSESSMENT_LICENSES.md`.
