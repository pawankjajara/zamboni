import os

from lib.settings_base import *
from mkt import asset_bundles


# We'll soon need a `settings_test_mkt` to override this.
APP_PREVIEW = True

WAFFLE_TABLE_SUFFIX = 'mkt'

# So temporary. Allow us to link to new devhub URLs from `Addon.get_dev_url()`.
MARKETPLACE = True

# 403 view to render for CSRF failures.
CSRF_FAILURE_VIEW = 'mkt.site.views.csrf_failure'

# Set log in/log out URLs for redirects to work.
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'

# Let robots tear this place up.
ENGAGE_ROBOTS = True

MKT_REVIEWERS_EMAIL = 'app-reviews@mozilla.org'
MKT_SENIOR_EDITORS_EMAIL = 'amo-admin-reviews@mozilla.org'
MKT_SUPPORT_EMAIL = 'marketplace-developer-support@mozilla.org'

ROOT_URLCONF = 'mkt.urls'

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.remove('api')
INSTALLED_APPS.remove('browse')
INSTALLED_APPS.remove('compat')
INSTALLED_APPS.remove('discovery')
INSTALLED_APPS.remove('devhub')
INSTALLED_APPS.remove('search')
INSTALLED_APPS = tuple(INSTALLED_APPS)

INSTALLED_APPS += (
    'mkt.site',
    'mkt.account',
    'mkt.browse',
    'mkt.detail',
    'mkt.developers',
    'mkt.experiments',
    'mkt.home',
    'mkt.inapp_pay',
    'mkt.purchase',
    'mkt.reviewers',
    'mkt.search',
    'mkt.stats',
    'mkt.submit',
    'mkt.support',
    'mkt.webapps',
    'devhub',  # Put here so helpers.py doesn't get loaded first.
)
SUPPORTED_NONAPPS += (
    '',  # Can you tell I'm really putting off bug 735120?
    'app',
    'apps',
    'dev',
    'home',
    'inapp_pay',
    'login',
    'logout',
    'privacy-policy',
    'purchases',
    'reviewers',
    'search',
    'settings',
    'submit',
    'support',
    'terms-of-use',
    'user',
    'users',
    'manifest.webapp',
)

SUPPORTED_NONLOCALES += (
    'manifest.webapp',
)

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
# TODO: I want to get rid of these eventually but it breaks some junk now.
# MIDDLEWARE_CLASSES.remove('mobility.middleware.DetectMobileMiddleware')
# MIDDLEWARE_CLASSES.remove('mobility.middleware.XMobileMiddleware')
# MIDDLEWARE_CLASSES.remove('cake.middleware.CookieCleaningMiddleware')
MIDDLEWARE_CLASSES += (
    'mkt.site.middleware.VaryOnAJAXMiddleware',
    # TODO: Remove when we flip `unleash-consumer`.
    'amo.middleware.NoConsumerMiddleware',
)

TEMPLATE_DIRS += (path('mkt/templates'),)
TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS)
TEMPLATE_CONTEXT_PROCESSORS.remove('amo.context_processors.global_settings')
TEMPLATE_CONTEXT_PROCESSORS += [
    'mkt.webapps.context_processors.is_webapps',
    'mkt.site.context_processors.global_settings',
    'mkt.experiments.context_processors.fragment',
]

# Tests.
NOSE_ARGS = [
    '--with-fixture-bundling',
    '--where=%s' % os.path.join(ROOT, 'mkt')
]

NO_ADDONS_MODULES = (
    'addons.views',
    'devhub.views.dashboard',  # The apps dashboard is a different view.
    'devhub.views.submit',  # Addon submit not ok, app submit a-ok.
    'browse.views.personas',
    'browse.views.extensions',
    'browse.views.language_tools',
    'browse.views.themes',
)

# Next level, no consumer for you!
NO_CONSUMER_MODULES = (
    'api',
    'bandwagon.views',
    'browse.views',
    'compat.views',
    'discovery.views',
    'files.views',
    'market.views',
    'piston',
    'users.views.edit',
    'users.views.purchases',
    'users.views.payments',
    'sharing.views',
    'tags.views',
    'versions.views',
    'mkt.account.profile',
    'mkt.webapps.views',
)

# Specific view modules and methods that we don't want to force login on.
NO_LOGIN_REQUIRED_MODULES = (
    'csp.views.policy',
    'csp.views.report',
    'mkt.developers',
    'mkt.submit',
    'django.views.i18n.javascript_catalog',
    'django.contrib.auth.views.password_reset',
    'django.contrib.auth.views.password_reset_done',
    'jingo.views.direct_to_template'
)

# Extend the bundles.
MINIFY_BUNDLES['css'].update(asset_bundles.CSS)
MINIFY_BUNDLES['js'].update(asset_bundles.JS)

CELERY_ROUTES.update({
    # Devhub.
    'mkt.developers.tasks.validator': {'queue': 'devhub'},
    'mkt.developers.tasks.fetch_manifest': {'queue': 'devhub'},
    'mkt.developers.tasks.fetch_icon': {'queue': 'devhub'},
    'mkt.developers.tasks.file_validator': {'queue': 'devhub'},

    # Images.
    'mkt.developers.tasks.resize_icon': {'queue': 'images'},
    'mkt.developers.tasks.resize_preview': {'queue': 'images'},
})

# Paths.
ADDON_ICONS_DEFAULT_PATH = os.path.join(MEDIA_ROOT, 'img/hub')
ADDON_ICONS_DEFAULT_URL = MEDIA_URL + '/img/hub'

# Feature flags.
POTCH_MARKETPLACE_EXPERIMENTS = False

# JWT identifier for this marketplace.
# This is used for in-app payments in two ways.
# 1. app must send JWTs with aud (the audience) set to this exact value.
# 2. apps will receive JWTs with iss (issuer) set to this value.
INAPP_MARKET_ID = 'marketplace.mozilla.org'

# If True, show verbose payment errors to developers.
# Consider this insecure.
INAPP_VERBOSE_ERRORS = False
