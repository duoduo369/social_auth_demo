AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.douban.Douban2Backend',
    'social_auth.backends.contrib.qq.QQBackend',
    'social_auth.backends.contrib.weibo.WeiboBackend',
    'social_auth.backends.contrib.renren.RenRenBackend',
    'social_auth.backends.contrib.baidu.BaiduBackend',
    'social_auth.backends.contrib.weixin.WeixinBackend',
    'social_oauth.backends.NickNameBackend',
    'django.contrib.auth.backends.ModelBackend',
)


TEMPLATE_CONTEXT_PROCESSORS += (
    'django.contrib.auth.context_processors.auth',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)


SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.partial.save_status_to_session',
    'social.pipeline.social_auth.save_authentication_user_detail_to_session',
)


SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect'
)

SOCIAL_AUTH_LOGIN_URL = '/login-url'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/logged-in'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/oauth/newassociation'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/new-error-url'
SOCIAL_AUTH_AUTHENTICATION_SUCCESS_URL = '/oauth/authentication/success'

SOCIAL_AUTH_WEIBO_KEY = ''
SOCIAL_AUTH_WEIBO_SECRET = ''
SOCIAL_AUTH_WEIBO_AUTH_EXTRA_ARGUMENTS = {'forcelogin': 'true'}
SOCIAL_AUTH_WEIBO_FIELDS_STORED_IN_SESSION = ['auth过程中的附加参数']

SOCIAL_AUTH_QQ_KEY = ''
SOCIAL_AUTH_QQ_SECRET = ''
SOCIAL_AUTH_QQ_FIELDS_STORED_IN_SESSION = ['auth过程中的附加参数']

SOCIAL_AUTH_DOUBAN_OAUTH2_KEY = ''
SOCIAL_AUTH_DOUBAN_OAUTH2_SECRET = ''

SOCIAL_AUTH_RENREN_KEY = ''
SOCIAL_AUTH_RENREN_SECRET = ''

SOCIAL_AUTH_BAIDU_KEY = ''
SOCIAL_AUTH_BAIDU_SECRET = ''

SOCIAL_AUTH_WEIXIN_KEY = ''
SOCIAL_AUTH_WEIXIN_SECRET = ''
SOCIAL_AUTH_WEIXIN_SCOPE = ['snsapi_login',]
