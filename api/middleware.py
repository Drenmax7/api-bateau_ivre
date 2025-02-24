from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()

class URLSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        csrftoken = request.GET.get("csrftoken")
        if csrftoken:
            request.META['HTTP_X_CSRFTOKEN'] = csrftoken
            request.COOKIES["csrftoken"] = csrftoken

        session_key = request.GET.get("sessionid")  # Récupère la clé de session dans l'URL
        #print(request.csrf_token)
        if session_key:
            session = SessionStore(session_key)
            if session.exists(session_key):
                user_id = session.get('_auth_user_id')
                if user_id:
                    try:
                        request.user = User.objects.get(pk=user_id)  # Authentifie l'utilisateur
                        request.session = session
                        #print("trouve",request.user)
                    except User.DoesNotExist:
                        #print("user does not exist")
                        request.user = AnonymousUser()
                else:
                    #print("no user id")
                    request.user = AnonymousUser()
            else:
                #print("sesion n'existe pas")
                request.user = AnonymousUser()
        else:
            #print("no session key")
            pass