# -*- coding: utf-8 -*-

各种导入

log = logging.getLogger(__name__)

class SocialOauthExceptionMiddleware(object):

    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            return self.handler_AuthAlreadyAssociated(request, exception)
        if isinstance(exception, NotAllowedToDisconnect):
            return self.handler_NotAllowedToDisconnect(request, exception)
        if isinstance(exception, (AuthException, SocialAuthBaseException)):
            return self.handler_AuthException(request, exception)
        if isinstance(exception, (RequestException,)):
            return self.handler_RequestException(request, exception)

    def handler_AuthAlreadyAssociated(self, request, exception):
        context = {}
        provider = PROVIDER_MAPPER.get(exception.backend.name, {}).get('platform', u'三方')
        msg = u'{provider}账号绑定失败'.format(provider=provider)
        reason = u'失败原因'
        context['failed_title'] = msg
        context['failed_content'] = reason
        return render_to_response('failed.html', context)

    def handler_NotAllowedToDisconnect(self, request, exception):
        context = {}
        msg = u'不能解绑此账号'
        long_message = u'失败原因'
        context['failed_title'] = msg
        context['failed_content'] = long_message
        return render_to_response('failed.html', context)

    def handler_AuthException(self, request, exception):
        context = {}
        msg = u'账号登陆失败'
        long_message = u'登陆失败，请稍后重试'
        context['failed_title'] = msg
        context['failed_content'] = long_message
        context['retry_url'] = '/跳转链接'
        context['retry_content'] = u'使用邮箱密码登陆'
        return render_to_response('failed.html', context)

    def handler_RequestException(self, request, exception):
        context = {}
        msg = u'账号登陆失败'
        long_message = u'登陆失败，请稍后重试。'
        context['retry_url'] = ''
        context['failed_title'] = msg
        context['failed_content'] = long_message

        return render_to_response('failed.html', context)
