---
name: migrate-chimera-plugin
description: >-
  Migrate or audit a chimera observatory plugin for Python 3.13 + the new
  chimera API + this cookiecutter template. Use when converting a legacy
  Python-2 chimera-* plugin (setup.py, camelCase API), or when checking that a
  plugin repo is compliant: src/ layout, snake_case API verified against the
  core interfaces, guarded hardware imports, SPDX/ruff/pre-commit, a preserved
  legacy branch, and a draft PR to astroufsc.
---

# Migrate / audit a chimera plugin (py2 → py3.13 + new API + template)

Convert a legacy Python-2 chimera plugin to Python 3.13, the new chimera
interfaces, and this template's layout — or audit an already-migrated plugin.
Work through the steps in order; the **Compliance checklist** at the end is the
audit form.

Core lives at `chimera/src/chimera/{interfaces,instruments,core,util}/`.
**Verify every ported call against that source. Never invent a method or
interface** — if the core lacks something (e.g. a polarimeter interface), stop
and flag it rather than guessing.

Gold-standard references to copy patterns from:
- `chimera-lna/src/chimera_lna/instruments/domelna.py` — migrated serial driver
- `chimera-pverify/src/chimera_pverify/controllers/pointverify.py` — migrated controller (proxies, image flow)
- `chimera-bisque` — migrated dual-mode (COM + TCP) telescope with live tests
- core `src/chimera/instruments/fake*.py` — mixin composition per instrument type
- core `tests/chimera/instruments/test_telescope.py` — Manager-based interface test

## 0. Prerequisites
- `uv tool install cruft`; `gh auth status` OK
- Identify the plugin's interface type (Telescope / Camera / Dome / Focuser /
  FilterWheel / WeatherStation / Switch / Lamp / Fan / controller)

## 1. Git setup — preserve history and the legacy code
- Remotes: `origin` = your fork (e.g. `wschoenell`), `upstream` = `astroufsc`.
  - If local `origin` points at astroufsc: `git remote rename origin upstream`,
    then `gh repo fork astroufsc/<repo> --clone=false` and
    `git remote add origin git@github.com:<you>/<repo>.git`.
  - `git fetch --all --prune`
- Preserve legacy: ensure a `legacy` branch exists on upstream
  (`git ls-remote upstream refs/heads/legacy`; if missing,
  `git push upstream upstream/master:refs/heads/legacy`).
- Branch: `git checkout -b py3 upstream/master`.
- Stash uncommitted WIP first (`git stash push -m "pre-migration wip"`). **Never
  `git clean` a repo you did not create** — inspect and preserve unknown work.

## 2. Two-commit structure (keeps the diff reviewable)
1. **Layout only, 100 % renames** — commit `adopt chimera-template project layout`:
   - `git rm setup.py README.rst`; `git rm -r docs licenses scripts` (boilerplate)
   - `mkdir -p src && git mv <pkg> src/<pkg>` — pure moves, zero content changes
   - generate the scaffold (step 3) and rsync template config over
2. **The port** — commit `port to python 3.13 and new chimera api`: code
   transforms, deps, tests.

Commit messages: short, imperative, lowercase. **Never add `Co-Authored-By`,
"Generated with", or any AI attribution** to commits or PRs.

## 3. Scaffold with cruft (not raw cookiecutter — `.cruft.json` enables updates)
```
uvx cruft create https://github.com/astroufsc/chimera-template --no-input \
  --extra-context '{"project_name":"<Name>","project_slug":"chimera-<x>",
  "package_name":"chimera_<x>","project_short_description":"...",
  "author_name":"...","author_email":"...","github_username":"astroufsc",
  "license":"GPL-2.0-or-later","include_instrument":"yes|no",
  "include_controller":"yes|no"}'
```
Generate in a scratch dir, delete the generated example stub module, then
`rsync -a --exclude .git --exclude uv.lock <gen>/chimera-<x>/ <repo>/`.
`project_slug`/`package_name` must match the repo name exactly.

## 4. API transform cheat sheet (check each against core; do not invent)
- `self.getManager().getProxy(loc)` → `self.get_proxy(loc)` (getManager is GONE)
- `getImageServer(self.getManager())` → `get_image_server(self)`
- All interface methods/events camelCase → snake_case (`slewToRaDec`→`slew_to_ra_dec`,
  `moveTo`→`move_to`, `exposeComplete`→`expose_complete`, …). `@event`/`@lock`
  imports unchanged.
- **Event signatures changed — confirm each in the interface file:**
  - `slew_begin(ra, dec, epoch)`, `slew_complete(ra, dec, status)`,
    `tracking_stopped(status)`, `park_complete()` (no args)
  - `readout_complete(image_url, status)` — a URL string now; parse with
    `Image.from_url(url)`. `camera.expose()` returns a tuple of URL strings.
  - `image.download()` does **not** exist in current core — use the static
    `ImageUtil.download(image)`.
- **WeatherStation:** `WSValue` removed; methods return plain floats in canonical
  units (°C, %, Pa, m/s, deg, mm/h, arcsec); `isRaining()`→`is_raining()`;
  `WeatherBase`→`WeatherStationBase`; compose mixins
  `WeatherTemperature/Humidity/Pressure/Wind/Rain/Safety/Seeing/Transparency`.
- **Camera:** `CameraBase` hooks `_expose`/`_readout`/`_save_image`/
  `_get_readout_mode_info`; the `CCD` enum is GONE; `ReadoutMode` attrs are
  `pixel_width`/`pixel_height`; abort via `self.abort.is_set()`.
- **Telescope:** implement `get_ra`/`get_dec`/`get_alt`/`get_az` (base raises
  `NotImplementedError`; controllers call `get_ra()`) — delegate to
  `get_position_ra_dec`/`get_position_alt_az`.
- **Enums:** positional `Enum("IN","OUT")` factory → class-style StrEnum
  (`class Direction(Enum): IN = "IN"`).
- **JD→datetime:** `chimera.core.site.datetimeFromJD` GONE →
  `astropy.time.Time(jd, format="jd").to_datetime()`.
- **Removed modules** — delete or rewrite code that imports them:
  `chimera.core.callback`, direct `chimera.core.manager.Manager`,
  `chimera.core.systemconfig` (typically in py2 `__main__` test harnesses).
- **Base class shape:** `class FooBase(ChimeraObject, Foo)`, then the concrete
  driver multiply-inherits the capability mixins (see `fake*.py`).

## 5. Python 2 → 3.13 syntax
- `except X, e:` → `except X as e:`
- `print` statements → logging / f-strings; `%`-format → f-strings (ruff `UP`)
- `SocketServer`→`socketserver`, `Queue`→`queue`, `urllib2`→`urllib.request`,
  `.iteritems()`→`.items()`, drop `from __future__`
- `datetime.utcnow()` → `datetime.now(datetime.UTC)`
- `0666` → `0o666`; `threading.currentThread().getName()` →
  `current_thread().name`; `Event.isSet()` → `Event.is_set()`
- `telnetlib` was **removed in 3.13** → vendor CPython 3.12's `telnetlib.py`
  into the package, or use `telnetlib3`

## 6. Third-party libraries
- **pyserial 3.x:** `flushInput()`→`reset_input_buffer()`,
  `flushOutput()`→`reset_output_buffer()`, `isOpen()`→`.is_open`; read/write are
  bytes (encode/decode). Prefer `serial.serial_for_url(self["device"])` — it
  supports `socket://host:port` simulators.
- **pymodbus 3.x:** `from pymodbus.client.sync import ...` →
  `from pymodbus.client import ...`; `resp.getRegister(0)` → `resp.registers[0]`.
- **ctypes:** `c_char_p` needs bytes; decode with `.value.decode()`.

## 7. Hardware-free import + optional/gated deps
- The **constructor must not touch hardware** — move device I/O to `__start__`.
  The class must instantiate with no hardware present.
- **Guard platform / optional imports so the module imports everywhere:**
  ```python
  if sys.platform == "win32":
      from win32com.client import Dispatch
      from pywintypes import com_error
  else:
      Dispatch = None
      com_error = Exception  # so @com-wrapped methods don't NameError
  ```
  For vendor SDKs (FLI, SBIG): wrap the import in `try/except ImportError` → set
  to `None`, and raise a clear error in `__start__` if missing.
- **pyproject deps:** port `install_requires` with version floors; drop py2-only
  deps. Platform-gate optional ones:
  ```toml
  [project.optional-dependencies]
  windows = ["pywin32>=306; sys_platform == 'win32'"]
  ```

## 8. Robustness for networked / scripting-API drivers
Lessons from drivers that talk to an external app (e.g. TheSkyX over TCP):
- **Timeout every socket/network call** — a hung peer must raise, never block
  forever.
- **The constructor connects nothing**; connect in `__start__`, and make the
  module import without the peer running.
- **Wrap remote calls in the remote API's own error handling.** For TheSkyX,
  wrap each JavaScript command in a `try/catch` and return the error as data —
  an uncaught script exception drops TheSkyX into its interactive debugger,
  which wedges the whole command queue.
- Handle the API's post-abort / busy states explicitly (retry transient "busy",
  treat "process aborted" as "stopped").

## 9. SPDX headers + lint
- Every `.py` starts with:
  ```python
  # SPDX-FileCopyrightText: <first-commit-year>-present <Author> <email>
  # SPDX-License-Identifier: GPL-2.0-or-later
  ```
  First-commit year: `git log --reverse --format=%ad --date=format:%Y | head -1`.
  Keep the original author when a legacy header names one.
- `uv sync && uv run ruff check --fix . && uv run ruff format . && uv run pre-commit run --all-files`
- If a `.history/` (VS Code local history) dir exists, exclude it from ruff
  (`[tool.ruff] extend-exclude = [".history"]`).

## 10. Verify
- `uv run python -c "import chimera_<x>"`
- Instantiate every public class hardware-free and read a config key.
- ruff clean; pre-commit clean.
- **Interface-level test (preferred):** drive the instrument inside a real
  `Manager` with a `Site`, proxied over the bus, so lifecycle
  (`__start__`/`__stop__`), config, `site()`, events and locks are all
  exercised — model it on core `test_telescope.py` and `fake*.py`. Build the bus
  with `Bus("tcp://127.0.0.1:<free-port>")`, run `bus.run_forever()` in a daemon
  thread, `manager.add_class(...)` (it returns the proxy).
- **Gate live/hardware tests on an env var** (e.g. `THESKYX_TEST_URL`); gate
  mount-moving / disruptive ones behind a second flag (e.g.
  `THESKYX_TEST_DESTRUCTIVE=1`) so a default run can't disturb real hardware.

## 11. Commit, push, PR
- Push `py3` to your fork.
- `gh pr create --repo astroufsc/<repo> --base master --head <you>:py3 --draft`
- PR body: template layout adoption, API port summary,
  "Legacy Python 2 code is preserved on the `legacy` branch.", exactly what was
  verified, and "Not tested against real hardware" where applicable.

---

## Compliance checklist (audit an already-migrated repo)
- [ ] `src/` layout; `pyproject.toml` (hatchling); `.cruft.json` present
- [ ] `requires-python >= 3.13`; no `setup.py`
- [ ] ruff (`N, I, UP, F`) + SPDX-copyright regex clean; pre-commit clean
- [ ] every API call and import exists in current core (no invented methods, no
      removed modules); snake_case throughout; enums are class-style StrEnum
- [ ] constructor works with no hardware; device I/O only in `__start__`
- [ ] module imports on non-target platforms (COM / vendor-SDK imports guarded);
      optional deps platform-gated in pyproject
- [ ] networked drivers time out and handle the peer's error/busy states
- [ ] SPDX header on every `.py`; original authors preserved
- [ ] `legacy` branch on upstream; no AI attribution anywhere in history
- [ ] hardware-free import/instantiate verified; interface-level test present
      (Manager + Site), live tests env-gated
- [ ] draft PR to `astroufsc/<repo>` with a verification summary
