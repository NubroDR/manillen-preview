# Manillen preview

This repository hosts the read-only GitHub Pages preview used to rehearse the migration from the current Shinylive mirror to the static mirror. The current `docs/` export is the existing public site, retained as a baseline for the service-worker test.

The Pages workflow deploys `docs/` from `main`. Before upload, it applies `prepare_legacy_pages.py` to the deployment artifact. Static exports are left unchanged; a legacy Shinylive export is guarded so the viewer starts only after its service-worker controller is ready, making rollback's first load reliable.

Only the existing public mirror snapshot belongs here; do not copy NAS data, source CSVs, backups, or private reports into this repository. The static site removes the prior Shinylive worker and its cache entries for this path only.

Preview URL: <https://nubrodr.github.io/manillen-preview/>

Production site: <https://nubrodr.github.io/Manillen/>
