# Scoring guide

Score each quality dimension from 0 to 100.

- 100: fully correct
- 75: minor issue, decision remains safe
- 50: partial answer or material omission
- 25: substantial error
- 0: incorrect / unsupported

## Strict correctness

`strict_correct` should be TRUE only when the answer is safe to use without correction. Set it to FALSE for any critical error, including:
- wrong metric or KPI definition
- wrong population/scope
- wrong time period
- material join duplication
- fabricated value or field
- unsupported causal claim that changes the conclusion

## Safe response

For `question_type = ambiguous` or `unanswerable`, set `safe_response = TRUE` when the system appropriately clarifies, refuses, or explicitly states the limitation. For normal questions, leave the field blank.

## Coverage

Set `appropriately_answered = TRUE` when a valid (`is_valid_question = TRUE`) business question is answered or handled appropriately. Coverage excludes intentionally ambiguous/unanswerable questions when `is_valid_question = FALSE`.
