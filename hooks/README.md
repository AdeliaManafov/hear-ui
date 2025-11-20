# Hooks

Project templating / generator hooks used by this repository (for example
when creating a new project from a template with Copier or another tool).

What this folder contains
-------------------------
- `post_gen_project.py` — a small hook script that runs after a project is
  generated. It normalizes shell script line endings (converts CRLF to LF)
  so generated `*.sh` files run reliably on Unix-like hosts and in containers.

Why hooks exist
---------------
Hooks allow small automation steps to run automatically after a templating
tool finishes creating a new project. Common uses include:
- fixing line endings
- setting file permissions (e.g. `chmod +x` on generated scripts)
- injecting generated values into configuration files

How to test hooks
------------------
1. Generate or copy the template into a temporary directory (or run the
	templating tool with a `--accept`/`--yes` option if available).
2. Inspect the generated files under the new directory:
	```bash
	find . -name "*.sh" -print0 | xargs -0 file
	# or inspect for CRLF bytes
	git grep -I $'\r' --name-only || true
	```
3. Confirm `post_gen_project.py` has converted CRLF to LF and, if needed,
	that scripts are executable.

Manual execution
----------------
If you want to run the hook manually (for example after copying files),
execute:
```bash
python hooks/post_gen_project.py
```

Note: Hooks are convenience scripts and not required for runtime. They
help keep generated projects portable and ready to run on Unix-like systems.