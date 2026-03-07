# Scripts Module
This module contains operational automation scripts for the research-skills audit pipeline.
Each script has a single operational responsibility and writes explicit machine-readable reports.
All refresh stages are designed for deterministic, auditable reruns.

## File List & Responsibilities
- `build_repo_inventory.py`: parse root thematic markdown files (`^0[1-6]_.*.md`) into validated inventory rows.
- `refresh_repo_snapshots.py`: refresh shallow git refs for inventory repos/branches in a short cache path.
- `materialize_evidence_files.py`: read evidence blobs from git refs and write staged output tree for `LATEST`.
- `verify_refresh_result.py`: verify staged output against inventory (row existence + repo set consistency).
- `cutover_latest.py`: publish staged `LATEST` via backup-and-rename cutover with rollback.
- `recover_missing_paths.py`: apply multi-strategy recovery for unresolved paths after materialization.
- `refresh_pipeline_common.py`: shared parsing/path/json helpers for all refresh scripts.
- `cleanup_theme02.py`: legacy cleanup utility for theme-02 generated data.
- `update_theme02.py`: legacy theme-02 document update utility.
- `update_04.py`: legacy theme-04 update utility.

Mandatory directive:
If files are added/removed in this directory or core responsibilities change, you must immediately update this list.
