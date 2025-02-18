from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChaloupeAPIView,ConnexionAPIView,EvenementAPIView,PartSocialAPIView, SocietaireAPIView, UtilisateurAPIView
from .populate import populate

router = DefaultRouter()
router.register(r"chaloupe", ChaloupeAPIView)
router.register(r"connexion", ConnexionAPIView)
router.register(r"evenement", EvenementAPIView)
router.register(r"partSocial", PartSocialAPIView)
router.register(r"societaire", SocietaireAPIView)
router.register(r"utilisateur", UtilisateurAPIView)

urlpatterns = [
    path("", include(router.urls)),
]

from django.conf import settings

if settings.DEBUG:
    print("========================================================\n"+
          "POPULATE EST ACCESSIBLE : METTRE DJANGO EN DEBUG = FALSE \n"+
          "========================================================")
    urlpatterns.append(
        path("populate/", populate),
    )