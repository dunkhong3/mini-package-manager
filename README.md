# Mini Package Manager

A small package manager written in Python to show how `add` and `install` work
under the hood: declaring a dependency, resolving the full dependency graph
(including circular dependencies), and placing every needed package version in
a local `node_modules` folder.

## How it works

```text
add("A@1.0.0")     -> writes the dependency into local_packages/package.json
install()          -> reads package.json, walks the dependency graph, copies
                      each needed package version into local_packages/node_modules
```

- **The registry** (`package_repo/registry/*.yaml`) stands in for a remote
  package index: one YAML file per package listing its versions, what each
  version depends on, and where its files live.
- **Resolution** is a depth-first walk over `package@version` nodes with a
  visited set, so a cycle such as `A@1.0.0 -> B@2.0.0 -> D@1.1.0 -> A@1.0.0`
  is installed once and never loops.
- **Several versions of one package can coexist** when different dependants
  need different versions; each is installed under its own version.

The sample registry has four packages (A, B, C, D) with three versions each,
deliberately wired with circular dependencies for testing.

## Run it

Requires Python 3.9+ and PyYAML:

```bash
pip install -r requirements.txt
python3 package_manager/main.py
```

`main.py` adds `A@1.0.0` and `C@1.1.0`, then installs. Expected output:

```text
Added package 'A' version '1.0.0' to dependencies.
Added package 'C' version '1.1.0' to dependencies.
Installed package D version 1.1.0 to node_modules
Installed package B version 2.0.0 to node_modules
Installed package C version 1.1.0 to node_modules
Installed package A version 1.0.0 to node_modules
Installed package C version 2.0.0 to node_modules
All dependencies installed successfully.
```

Edit the `add(...)` calls in `main.py` to try other combinations.

## Project layout

```text
package_manager/
  add.py              add a package@version to package.json
  install.py          resolve the dependency graph and install everything
  main.py             example entry point
package_repo/
  registry/           one YAML per package: versions, dependencies, download path
  metadata/           the "downloadable" package contents (one text file per version)
local_packages/
  package.json        the project's declared dependencies
  node_modules/       where installed packages land (ignored by git)
```

## Limitations and next steps

- Paths are relative to the working directory; a config file or container
  would make them explicit.
- Little error handling: unknown packages or versions and a malformed
  `package.json` are not reported cleanly.
- No tests yet; the dependency resolver and the cycle handling are the first
  things to cover.
- A real package manager would add conflict resolution between incompatible
  version requirements, a lock file for reproducible installs, a download
  cache, and checksums to verify package integrity.
