from .base import *

# Security

# XSS
SECURE_BROWSER_XSS_FILTER = True

# CSP
MIDDLEWARE += [
    'csp.middleware.CSPMiddleware'
]

CSP_DEFAULT_SRC = ("'none'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "https://cdn.jsdelivr.net",)
CSP_IMG_SRC = ("'self'", "https://m.media-amazon.com", "https://th.bing.com", "https://pics.filmaffinity.com", "https://i.ebayimg.com")
CSP_OBJECT_SRC = ("'none'",)
CSP_MEDIA_SRC = ("'none'",)
CSP_FRAME_SRC = ("'none'",)
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_BASE_URI = ("'none'",)
CSP_FORM_ACTION = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_BLOCK_ALL_MIXED_CONTENT = True

# X-Frame
X_FRAME_OPTIONS = 'DENY'

# X-Content-Type
SECURE_CONTENT_TYPE_NOSNIFF = True

# Referrer Policy
SECURE_REFERRER_POLICY = 'same-origin'

