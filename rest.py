from django_restapi.model_resource import Collection
from django_restapi.responder import XMLResponder
from django_restapi.resource import Resource
from django_restapi.authentication import *

from django.contrib.auth.models import User
from django.shortcuts import render_to_response,get_object_or_404

from compsoc.games.models import Game

#class UserEntry(Resource):
#    def read(self, request, user_id):
#        context = {'friendship':get_object_or_404(}
#        return render_to_response('xml/user.xml', context)

xml_user = Collection(
    queryset = User.objects.all(),
    permitted_methods = ('GET',),
    expose_fields = ('first_name','last_name','is_staff'),
    responder = XMLResponder(),
    authentication = HttpBasicAuthentication()
)

xml_games = Collection(
    queryset = Game.objects.all(),
    permitted_methods = ('GET',),
    responder = XMLResponder(),
)
