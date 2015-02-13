# -*- coding: utf-8 -*-
import hashlib
import re
import urllib
import logging
from functools import wraps

from django.contrib.auth.models import make_password, User

from social.exceptions import AuthAlreadyAssociated
from social.pipeline.social_auth import associate_user
from social_auth.exceptions import NotAllowedToDisconnect
from social_auth.models import UserSocialAuth
from social_auth.views import load_strategy
from util.string_utils import ALL_NUMBER_RE, PHONE_NUMBER_RE


PROVIDER_MAPPER = {
    'weibo': {
        'platform': u'微博',
        'name': 'name',
    },
    'qq': {
        'platform': u'qq',
        'name': 'nickname',
    },
    'douban-oauth2': {
        'platform': u'豆瓣',
        'name': 'uid',
    },
    #'douban': u'豆瓣',
    'weixin': {
        'platform': u'微信',
        'name': 'nickname',
    },
    'renren': {
        'platform': u'人人',
        'name': 'name',
    },
    'baidu': {
        'platform': u'百度',
        'name': 'uname',
    },
}


def get_strategy(provider):
    '''
    provider:
        type: str
        example: weibo
    '''
    return load_strategy(backend=provider)


def get_uid(strategy, detail):
    return strategy.backend.get_user_id(None, detail)


def new_associate_user(strategy, uid, user, extra_data=None):
    if UserSocialAuth.objects.filter(user=user, provider=strategy.backend.name).exists():
        raise AuthAlreadyAssociated(strategy.backend)
    if not extra_data:
        extra_data = {}
    result = associate_user(strategy, uid, user=user)
    sc_user = result['social']
    if sc_user:
        sc_user.extra_data = extra_data
        sc_user.save()
    return sc_user



def check_can_unbind_social_account(user):
    if user.password == make_password(None):
        if UserSocialAuth.objects.filter(user=user).count() == 1:
            raise NotAllowedToDisconnect(u'只有一个三方账号，不能解绑')
    return True


def social_account_bind_status(user):
    social_accounts = UserSocialAuth.objects.filter(user=user)
    status = {}
    for provider in PROVIDER_MAPPER:
        status[provider] = {
            'bind': False,
            'name': '',
        }

    for sa in social_accounts:
        try:
            provider = sa.provider
            provider_status = status[provider]
            provider_status['bind'] = True
            provider_status['name'] = sa.extra_data.get(
                PROVIDER_MAPPER[provider]['name'],
                u'{}平台账号'.format(provider)
            )
        except KeyError as ex:
            logging.error(ex)

    # 用户是否可以解绑三方账号
    # 逻辑：如果没有邮箱，并且只有一个三方账号，不可解绑
    # TODO: 接入手机号后修改此处逻辑
    can_unbind = True
    if not user.email and social_accounts.count() <= 1:
        can_unbind = False

    return (status, can_unbind)


def clean_oauth_session(field):
    def _clean(func):
        @wraps(func)
        def _wrap(*args, **kwargs):
            request = args[0]
            for f in field:
                request.session[f] = ''
            response = func(*args, **kwargs)
            return response
        return _wrap
    return _clean
