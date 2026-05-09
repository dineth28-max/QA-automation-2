# QA Automation

This folder contains the Maven Selenium suite that validates the deployed Mango Drink app.

## Run locally

```bash
mvn test -Dapp.baseUrl=http://192.99.71.97:6666
```

Optional overrides:

```bash
mvn test \
  -Dapp.baseUrl=http://192.99.71.97:6666 \
  -Dapp.username=dineth \
  -Dapp.password=dineth@123
```

The test runs Chrome in headless mode, fills the login form, and confirms the authenticated landing page loads.

## Triggering from the deploy repository

This repository exposes a workflow that listens for `repository_dispatch` events with the `run-qa-tests` type. The deploy pipeline sends a dispatch with a payload containing `app_url`, `username`, and `password`.

On GitHub Actions you can access those values in the QA workflow via `github.event.client_payload.app_url`, `github.event.client_payload.username`, and `github.event.client_payload.password`.

Example minimal dispatch payload sent by the deploy repo:

```json
{"app_url":"https://192.99.71.97:6666","username":"dineth","password":"dineth@123"}
```