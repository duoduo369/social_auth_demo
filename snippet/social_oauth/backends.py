from django.contrib.auth.backends import ModelBackend
from 你个人的.models import UserProfile
from social_auth.models import UserSocialAuth

class OAuth2Backend(ModelBackend):
    '''
    oauth backend
    '''

    def authenticate(self, provider=None, uid=None):
        try:
            user_social = UserSocialAuth.objects.get(provider=provider, uid=uid)
            return user_social.user
        except UserSocialAuth.DoesNotExist:
            return None
