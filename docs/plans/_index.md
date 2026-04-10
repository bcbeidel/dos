# Plans


| File | Description |
| --- | --- |
| [2026-03-21-data-pipeline-research-context.plan.md](2026-03-21-data-pipeline-research-context.plan.md) | Run structured research and distillation across 23 data pipeline characteristic areas, producing grounded context documents that underpin the dos skill library. |
| [2026-03-23-foundation-evaluate-source.plan.md](2026-03-23-foundation-evaluate-source.plan.md) | Scaffold the skill architecture and implement dos:evaluate-source end-to-end, validating directory conventions, SKILL.md constraints, reference curation, artifact templates, and scripts. |
| [2026-03-23-scope-design-skills.plan.md](2026-03-23-scope-design-skills.plan.md) | Implement 5 skills (scope-data-product, select-model, define-contract, assess-quality, design-pipeline) following the validated pattern from evaluate-source. |
| [2026-03-23-build-phase-skills.plan.md](2026-03-23-build-phase-skills.plan.md) | Implement 2 Build-phase skills (implement-source, implement-models) that generate code from data product specification artifacts. |
| [2026-03-23-verify-phase-review-pipeline.plan.md](2026-03-23-verify-phase-review-pipeline.plan.md) | Implement the final Tier 1 skill (dos:review-pipeline) that audits data pipelines against best practices. |
| [2026-04-08-implement-source-boundary-guardian.plan.md](2026-04-08-implement-source-boundary-guardian.plan.md) | Add runtime behavior modeling, mechanical raw-first enforcement, and cost-aware validation to implement-source. Consolidates #33, #30, #29, #26, #24, #16. |
| [2026-04-08-assess-quality-test-selection.plan.md](2026-04-08-assess-quality-test-selection.plan.md) | Add rule-type-to-dbt-test mapping reference to assess-quality, fixing wrong test suggestions (#31) and missing run-over-run patterns (#15). |
| [2026-04-10-pipeline-document-consolidation.plan.md](2026-04-10-pipeline-document-consolidation.plan.md) | Replace 6 per-pipeline DOS artifacts with data-product.md; collapse 9 skills into 4 (scope-source, scope-data-product, implement-source, implement-data-product). Closes #23. |
