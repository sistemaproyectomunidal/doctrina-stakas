# Security Checklist (minimum)

1. Never commit secrets. Add .env to .gitignore.
2. Use secret managers (GitHub Secrets, E2B, Vault).
3. Rotate any key that was exposed publicly immediately.
4. Use least privilege for tokens and service accounts.
5. Enable MFA/2FA on all accounts.
6. Monitor billing and usage dashboards for anomalies.
7. Restrict network access to production service accounts by IP where possible.
8. Review audit logs after deployment.
