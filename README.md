# QA Automation

This folder contains the Maven Selenium suite that validates the deployed Mango Drink app.

## Run locally

If your app container is published on port 8081, run:

```bash
mvn test -Dapp.baseUrl=http://localhost:8081 -Dapp.headless=false
```

If you want to target the deployed environment instead, use:

```bash
mvn test -Dapp.baseUrl=http://192.99.71.97:6666
```

To open a visible Chrome window on your machine instead of headless mode:

```bash
mvn test -Dapp.baseUrl=http://192.99.71.97:6666 -Dapp.headless=false
```

Optional overrides:

```bash
mvn test \
  -Dapp.baseUrl=http://192.99.71.97:6666 \
  -Dapp.username=dineth \
  -Dapp.password=dineth@123 \
  -Dapp.headless=false
```

The test runs Chrome in headless mode by default, fills the login form, and confirms the authenticated landing page loads.

## Pipeline command

The GitHub Actions workflow runs the same suite with:

```bash
mvn -B test
```

It expects `APP_BASE_URL`, `APP_USERNAME`, and `APP_PASSWORD` to be supplied by the dispatch payload.

## Triggering from the deploy repository

This repository exposes a workflow that listens for `repository_dispatch` events with the `run-qa-tests` type. The deploy pipeline sends a dispatch with a payload containing `app_url`, `username`, and `password`.

On GitHub Actions you can access those values in the QA workflow via `github.event.client_payload.app_url`, `github.event.client_payload.username`, and `github.event.client_payload.password`.

Example minimal dispatch payload sent by the deploy repo:

```json
{"app_url":"https://192.99.71.97:6666","username":"dineth","password":"dineth@123"}
```