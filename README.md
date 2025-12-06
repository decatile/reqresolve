# 📦 Pin Package Versions Based on Historical Requirements

A lightweight CLI tool that analyzes the history of a `requirements.txt` file in a Git repository and generates a new version of it, pinning each package to the **exact version that was available at the time of its last change**.

This is especially useful for:
- Reproducing old builds from historical code.
- Ensuring reproducibility when dependencies were locked by commit history.
- Debugging issues caused by outdated or incompatible dependency versions.

---

## 🔧 How It Works

1. **Finds the most recent change** to your `requirements.txt` file using Git blame (`git blame`).
2. For each package listed in the file:
    - Queries PyPI for all available releases.
    - Finds the latest version that was uploaded *before* the last change to the file.
3. Outputs a new `requirements.txt` with versions pinned like:
```txt
requests<=2.25.1
numpy<=1.20.0
   ```

> ✅ No need to manually track down old package versions — this tool does it automatically.

---

### Options

| Flag | Description                                                      |
|------|------------------------------------------------------------------|
| `-r`, `--root` | Path to the Git repository root (default: `.`)                   |
| `-f`, `--file` | Relative path to requirements file (default: `requirements.txt`) |

### Example

```bash
reqresolve \
  -r . \
  -f requirements.txt
```

This will:
- Analyze changes in `requirements.txt`
- Backup to `requirements.txt.bak`
- Generate a new file `requirements.txt` with pinned versions

---

## 📂 File Format Support

The tool supports standard package names and extras:

```txt
requests>=2.0.0
django[dev]==4.1.7
pyyaml<6.0
```

It correctly parses:
- `package`
- `package==version`
- `package>=version`
- `package[extra]` (e.g., `numpy[testing]`)
- `package[extra]==version`

> ⚠️ Only the base name is used to query PyPI. Extras are preserved in output.

---

## 🛡️ Safety & Features

- **Backups**: By default, it backs up your original file with `.bak` extension if overwriting.
- **No external state**: Works purely from Git history and PyPI metadata.
- **Async I/O**: Fast parallel queries to PyPI using `httpx`.
- **Rich CLI output**: Clear progress messages and status updates.

---

## 📌 Limitations

- Only works with packages hosted on [PyPI](https://pypi.org).
- Does not handle private repositories or custom indexes.
- Version resolution assumes that the *last change* to `requirements.txt` reflects when a dependency was locked — may be inaccurate if changes were made without updating versions.

---

## 📝 License

MIT — see [LICENSE](LICENSE) for details.

---

## 💬 Feedback & Contributions

Found a bug? Want new features (like support for `pipenv`, `poetry`, or custom indexes)?  
Open an issue or submit a pull request!

> ✨ **Contributions welcome!**
