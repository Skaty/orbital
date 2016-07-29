from social.backends.open_id import OpenIdAuth


class NUSOpenId(OpenIdAuth):
    """NUS OpenID authentication"""
    URL = 'http://openid.nus.edu.sg'
    name = 'nus'
    USERNAME_KEY = 'nickname'
