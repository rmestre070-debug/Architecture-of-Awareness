# Security Policy

## Supported Versions
The following versions of Scholarly Prompt Studio are currently supported with security updates:

| Version | Supported |
|---------|-----------|
| 2.x     | ✔ Active  |
| 1.x     | ✖ No      |

Older versions may continue to function but will not receive security patches.

---

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **Do not open a public GitHub issue.**
2. Email the maintainer directly at:  
   **<your-email-here>**
3. Include:
   - A clear description of the issue  
   - Steps to reproduce  
   - Potential impact  
   - Any suggested fixes (optional)

You will receive an acknowledgment within **72 hours**.

---

## Disclosure Policy

- Valid vulnerabilities will be addressed promptly.
- A fix will be prepared before any public disclosure.
- Credit will be given to the reporter unless anonymity is requested.

---

## Security Best Practices for Contributors

- Avoid committing sensitive data (API keys, credentials, personal info).
- Do not introduce dependencies with known vulnerabilities.
- Validate all plugin inputs and outputs.
- Follow Python security best practices (e.g., avoid `eval`, sanitize file paths).
- Test changes on both desktop and Android environments.

---

## Scope

This policy applies to:

- The core engine  
- The controller (`scholarly_studio.py`)  
- Plugin loading system  
- UI logic  
- Any bundled plugins  

It does **not** apply to:

- Third‑party plugins created by external developers  
- User‑generated content  
- External AI models or APIs