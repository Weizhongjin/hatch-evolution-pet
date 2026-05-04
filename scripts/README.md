# Script Inventory

- `pet_paths.py`: shared path constants for Codex home, machinespace, line data, and Desktop-facing pets.
- `pet_state.py`: default ledger schema plus load, save, init, and print helpers.
- `pet_usage_aggregate.py`: daily Codex Desktop token aggregation from local session JSONL data.
- `pet_progression.py`: XP computation, idempotent daily sync, level, and milestone accounting.
- `pet_prompt_state.py`: dialogue counters and sparse evolution reminder decisions.
- `pet_line_profile.py`: pet line profile creation and updates in machinespace.
- `pet_evolution_brief.py`: next-form evolution brief writer for generation handoff.
- `prepare_pet_run.py`: hatch-pet-compatible run folder, prompt, and imagegen job manifest preparation.
- `pet_job_status.py`: hatch-pet-compatible imagegen job readiness and completion status.
- `record_imagegen_result.py`: records selected generated images into the deterministic pet run.
- `derive_running_left_from_running_right.py`: mirrors running-right into running-left when explicitly safe.
- `finalize_pet_run.py`: extracts frames, composes the atlas, creates QA outputs, and packages the pet.
- `package_custom_pet.py`: writes Desktop-facing `pet.json` and `spritesheet.webp` packages.
- `compose_atlas.py`, `extract_strip_frames.py`, `inspect_frames.py`, `make_contact_sheet.py`, `queue_pet_repairs.py`, `render_animation_videos.py`, and `validate_atlas.py`: deterministic QA and packaging helpers carried forward from hatch-pet.

