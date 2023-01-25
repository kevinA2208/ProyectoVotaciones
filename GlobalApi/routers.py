from rest_framework.routers import DefaultRouter
from GlobalApi.views.usuarios_views import LiderViewSet
from GlobalApi.views.votantes_views import VotantesViewSet, TotalVotantesViewSet
from GlobalApi.views.puesto_votacion_views import PuestoVotacionViewSet
from GlobalApi.views.municipios_departamentos_views import MunicipiosViewSet, DepartamentosViewSet




router= DefaultRouter()
router.register(r'lideres', LiderViewSet, basename='lideres')
router.register(r'votantes', VotantesViewSet, basename='votantes')
router.register(r'puesto_votacion', PuestoVotacionViewSet, basename='puesto_votacion')
router.register(r'municipios', MunicipiosViewSet, basename='municipios')
router.register(r'departamentos', DepartamentosViewSet, basename='departamentos')
router.register(r'total_votantes', TotalVotantesViewSet, basename='total_votantes')





urlpatterns = router.urls



