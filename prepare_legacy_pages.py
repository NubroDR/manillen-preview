"""Make a generated Shinylive export wait for its service worker before startup."""

import argparse
from pathlib import Path


OLD_STARTUP = """    <script type="module">
      import { runExportedApp } from "./shinylive/shinylive.js";
      runExportedApp({
        id: "root",
        appEngine: "python",
        relPath: "",
      });
    </script>"""

SAFE_STARTUP = """    <script type="module">
      function waitWithTimeout(promise, message) {
        return new Promise((resolve, reject) => {
          const timeout = window.setTimeout(() => reject(new Error(message)), 10000);
          Promise.resolve(promise).then(
            (value) => {
              window.clearTimeout(timeout);
              resolve(value);
            },
            (error) => {
              window.clearTimeout(timeout);
              reject(error);
            },
          );
        });
      }

      async function waitForServiceWorkerController() {
        if (!("serviceWorker" in navigator)) return;
        await waitWithTimeout(
          navigator.serviceWorker.ready,
          "Timed out waiting for the Shinylive service worker.",
        );
        if (navigator.serviceWorker.controller) return;
        await waitWithTimeout(
          new Promise((resolve) => {
            navigator.serviceWorker.addEventListener("controllerchange", resolve, {
              once: true,
            });
          }),
          "Timed out waiting for the Shinylive service worker controller.",
        );
        if (!navigator.serviceWorker.controller) {
          throw new Error("Shinylive service worker controller is unavailable.");
        }
      }

      try {
        await waitForServiceWorkerController();
      } catch (error) {
        document.body.textContent =
          "De oude leesbare site kon niet starten. Ververs de pagina of probeer het later opnieuw.";
        throw error;
      }

      const { runExportedApp } = await import("./shinylive/shinylive.js");
      runExportedApp({
        id: "root",
        appEngine: "python",
        relPath: "",
      });
    </script>"""


def prepare_legacy_pages(site_dir):
    site_dir = Path(site_dir)
    if not (site_dir / "shinylive-sw.js").is_file():
        return False

    index_path = site_dir / "index.html"
    html = index_path.read_text(encoding="utf-8")
    if SAFE_STARTUP in html:
        return False
    if html.count(OLD_STARTUP) != 1:
        raise ValueError("Generated Shinylive index has an unexpected startup block.")

    index_path.write_text(html.replace(OLD_STARTUP, SAFE_STARTUP), encoding="utf-8")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Add a service-worker startup guard to a generated Shinylive export."
    )
    parser.add_argument("site_dir", type=Path)
    args = parser.parse_args(argv)
    changed = prepare_legacy_pages(args.site_dir)
    print("Legacy Shinylive startup guard added." if changed else "No legacy Shinylive export found or already guarded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
