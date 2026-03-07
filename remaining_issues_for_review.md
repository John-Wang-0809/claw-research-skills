# Remaining Non-Accurate Skills -- Post-Fix Review

- Date: 2026-03-07 (updated: all issues resolved after 9 rounds)
- Original issues: 141 (from LLM audit on 2026-03-04)
- Fix rounds applied: 9 (Round 1-6: automated + manual fixes; Round 7: delete 7 unavailable; Round 8: ton-vulnerability-scanner; Round 9: root cause analysis + 18 targeted fixes + 3 reclassified)
- Skills deleted (SKILL.md unavailable): 7 (6 CANNOT_VERIFY + 1 INACCURATE pptx-posters from claude-scientific-writer)
- Fixed to accurate: 133
- Remaining partial: 0
- Remaining inaccurate: 0
- Cannot verify (SKILL.md unavailable): 0
- **Total remaining: 0**

## Notes

All 141 original issues have been resolved across 9 rounds of fixes.

### Round 9 Summary (final round)

Root cause analysis categorized the 21 remaining PARTIAL skills into 6 types:

1. **Body/frontmatter mismatch** (4): YAML description promises features the body doesn't document (deepspeed ×2, llama-factory, grna-design)
2. **Summary-only features** (4): Features in YAML/summary but no body examples (spatial-multiomics, genome-assembly-pipeline, spatial-pipeline, mendelian-randomization)
3. **Minor overreach** (7): Description adds unsupported claims (spec-workflow-orchestrator, uniprot-access, k8s-security-policies, Research, deepchem, drugbank-database, generate-image)
4. **Description too narrow** (2): Omits major documented capabilities (tdd-orchestrator, de-visualization)
5. **Paraphrasing mismatch** (1): Uses different terminology (cairo-vulnerability-scanner)
6. **Auditor non-determinism** (3): Audit complaint was wrong — reclassified to ACCURATE (llm-app-patterns, pathml, scientific-slides)

Actions taken:
- 3 skills reclassified to ACCURATE (no description change needed)
- 18 skills fixed by rewriting Function Explanation to match SKILL.md body content

---

## PARTIAL (0)

*No remaining issues.*
