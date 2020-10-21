from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User, auth

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        print("entered in pre soc")
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """

        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            print("111st loop")
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            if 'email' not in User:
                return
            else:
                # check if given email address already exists.
                # Note: __iexact is used to ignore cases
                print("beforree ttryyy")
                try:
                    print("entered try")
                    email = sociallogin.account.extra_data['email'].lower()
                    print("emaaailll",email)
                    print("ussesr emmm",user.email)
                    email_address = EmailAddress.objects.get(email__iexact=email)


                # if it does not, let allauth take care of this new social account
                except EmailAddress.DoesNotExist:
                    return

                # if it does, connect this new social login to the existing user
                user = email_address.user
                sociallogin.connect(request, user)
            return
        
        

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        print("beforree ttryyy")
        try:
            print("entered try")
            email = sociallogin.account.extra_data['email'].lower()
            print("emaaailll",email)
            print("ussesr emmm",user.email)
            email_address = EmailAddress.objects.get(email__iexact=email)


        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        user = email_address.user
        sociallogin.connect(request, user)