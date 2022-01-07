export CLA_E2E_BACKEND_URL=http://localhost:8010
export CLA_E2E_FRONTEND_URL=http://localhost:8011
export CLA_E2E_SELENIUM_WEB_DRIVER_URL=http://localhost:9515

exec behave "$@"
