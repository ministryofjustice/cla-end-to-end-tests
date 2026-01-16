export BROWSER=chrome
export USING_CHROME_DRIVER=True
export CHROME_DRIVER_LOCATION="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
#these directories need to be overridden as they do not get picked up from cla-end-to-end-tests
# UPDATE YOUR /etc/hosts to include the following snippet
# 127.0.0.1   clabackend
# 127.0.0.1	  clafrontend
# 127.0.0.1   clapublic
export CLA_E2E_BACKEND_URL=http://clabackend:8010
export CLA_E2E_FRONTEND_URL=http://clafrontend:8011
export CLA_E2E_SELENIUM_WEB_DRIVER_URL=http://localhost:9515
export CALL_CENTRE_CLIENT_ID=b4b9220ffcb11ebfdab1
export CALL_CENTRE_SECRET_ID=2df71313bdd38a2e1b815015e1b14387e7681d41
export CALL_CENTRE_TEST_USER=cla_operator
export CLA_PROVIDER_CLIENT_ID=59657ed22d980251cdd3
export CLA_PROVIDER_SECRET_ID=0494287c65bdf61d29f0eeed467ec8e090f0d80f

exec behave "$@"