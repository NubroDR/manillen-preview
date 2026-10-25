# Manillen preview

This repository hosts the read-only GitHub Pages preview used to rehearse the migration from the current Shinylive mirror to the static mirror. The first commit preserves the previous public Shinylive export for the service-worker rehearsal; `docs/` on `main` now contains the static mirror built from the existing public snapshot.

The Pages workflow deploys `docs/` from `main`. Only the existing public mirror snapshot belongs here; do not copy NAS data, source CSVs, backups, or private reports into this repository. The static site removes the prior Shinylive worker and its cache entries for this path only.

Preview URL: <https://nubrodr.github.io/manillen-preview/>

Production site: <https://nubrodr.github.io/Manillen/>
