各种导入

logger = logging.getLogger(__name__)


def _new_association(strategy, detail, user):
    '''
    绑定用户与三方oauth时使用此接口, 返回social_user
    '''
    uid = get_uid(strategy, detail)
    sc_user = new_associate_user(strategy, uid, user, detail)
    if not sc_user:
        logger.error('new association create social user failed!')
    return sc_user


def new_association(request):
    # 这个东西我已经在python-social-auth里面实现了，因此你可以在这里做更多的事情
    detail = request.session.get('authentication_user_detail')
    provider = detail['social_provider']
    strategy = get_strategy(provider)
    _new_association(strategy, detail, request.user)
    provider_platform = PROVIDER_MAPPER.get(provider, {}).get('platform', u'三方')
    context = {'provider': provider_platform}
    return render_to_response('oauth_bind_success.html', context)


def _unbind_social(user, provider):
    # oauth用户默认密码为！，如果没改过密码则此用户不可能通过邮箱
    # 用户名密码的方式登录进来
    check_can_unbind_social_account(user)
    provider_social = UserSocialAuth.objects.filter(user=user, provider=provider)
    if provider_social.exists():
        provider_social.delete()

@require_POST
@login_required
def unbind_social(request, backend):
    js = {'success': False, 'messages': {}}
    try:
        _unbind_social(request.user, backend)
        js['success'] = True
    except NotAllowedToDisconnect as ex:
        js['messages'][backend] = ex.message
    return JsonResponse(js)


@transaction.commit_on_success
def _get_or_create_oauth_user(strategy, detail):
    '''
    strategy -- strategy obj
    detail -- oauth登录拿到token时的response
    '''
    uid = get_uid(strategy, detail)
    # weibo新接口uid改名叫做id
    if not uid:
        uid = detail.get('id')
    result = social_user(strategy, uid)
    backend = strategy.backend
    _created = False
    # 已有账户，直接登录
    if result['user']:
        user = result['user']
    # 否则创建用户，之后登录
    else:
        user = User()
        user.username = str(uuid.uuid4()).replace('-', '')[:20]
        user.email = None
        user.is_active = True
        user.set_unusable_password()
        user.save()
        extra_data = backend.extra_data(user, uid, detail, {})
        profile = UserProfile(user=user)
        nickname = extra_data['username']
        profile.phone_number = None
        profile.nickname = nickname
        profile.unique_code = profile.get_unique_code()
        if extra_data.get('profile_image_url'):
            profile.avatar = extra_data['profile_image_url']
        profile.save()
        new_associate_user(strategy, uid, user, detail)
        _created = True
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    return (user, _created)


@ensure_csrf_cookie
def authentication_success(request):
    '''
    新用户注册时
    用户直接走oauth后通过python-social-auth的auth后，成功会回调到此处，
    此时django的用户应该是未登录状态 request.user.is_authenticated() is False
    '''
    detail = request.session.get('authentication_user_detail')
    provider = detail['social_provider']
    strategy = get_strategy(provider)
    enrollment_action = request.session.get('enrollment_action')
    course_id = request.session.get('course_id')
    user, _created = _get_or_create_oauth_user(strategy, detail)
    login(request, user)
    user_profile = user.profile
    user_profile.last_login_ip = request.META.get('REMOTE_ADDR', None)
    user_profile.save()
    # 如果用户没有登录就选课，并且这时候选择的是oauth，尝试enroll课程
    if enrollment_action:
        request.method = 'POST'
        request.POST = request.POST.copy()
        request.POST['enrollment_action'] = enrollment_action
        request.POST['course_id'] = course_id
        try_change_enrollment(request)
    context = {'next': request.session.get('next', '')}
    return render_to_response('oauth_login_success.html', context)


@clean_oauth_session(['next', 'enrollment_action', 'course_id'])
def oauth_login(request, backend):
    '''
    注册和登录时都不应该是登录后的状态
    '''
    if request.user.is_authenticated():
        return redirect(reverse('/'))
    return auth(request, backend)


@clean_oauth_session(['next', 'enrollment_action', 'course_id'])
def oauth_register(request, backend):
    '''
    注册和登录时都不应该是登录后的状态
    '''
    if request.user.is_authenticated():
        return redirect(reverse('/'))
    return auth(request, backend)

@clean_oauth_session(['next',])
@login_required
def oauth_bind(request, backend):
    '''
    绑定时需要时登录状态
    '''
    return auth(request, backend)
