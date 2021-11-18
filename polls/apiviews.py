"""
To start with, we will use the APIView to build the polls list and poll detail API we built in the chapter, A simple API
with pure Django.

"""

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer,UserSerializer
from django.contrib.auth import authenticate



# class PollList(APIView):
#     def get(self,request):
#         polls = Poll.objects.all()[:20]
#         data = PollSerializer(polls, many=True).data
#         return Response(data)



# class PollDetail(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         data = PollSerializer(poll).data
#         return Response(data)



""" Using DRF generic views to simplify code, so change our apiviews.py to have the following instead of the above"""


from rest_framework import generics





class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer



class PollDetail(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

""" Adding a view to create choices for voting nut importing them first above"""

# class ChoiceList(generics.ListCreateAPIView):
#     queryset = Choice.objects.all()
#     serializer_class = ChoiceSerializer


# class CreateVote(generics.CreateAPIView):
#     serializer_class = VoteSerializer

"""
CHAPTER 6: More Views and ViewSets=>[to have a better url structure] {
    We have three API endpoints
• /polls/ and /polls/<pk>/
• /choices/
• /vote/
They get the work done, but we can make our API more intuitive by nesting them correctly. Our redesigned urls look
like this:
• /polls/ and /polls/<pk>
• /polls/<pk>/choices/ to GET the choices for a specific poll, and to create choices for a specific poll.
(Idenitfied by the <pk>)
• /polls/<pk>/choices/<choice_pk>/vote/ - To vote for the choice identified by <choice_pk>
under poll with <pk>.
}
"""
# therefore our new apiviews will look like these with ChoiceList and CreateVote changed as follows;

from rest_framework import status

class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    serializer_class = ChoiceSerializer


class CreateVote(APIView):
    serializer_class = VoteSerializer

    def post(self,request,pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice':choice_pk, 'poll':pk, 'voted_by':voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Introducing Viewsets and Routers

from rest_framework import viewsets

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer



class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer



class LoginView(APIView):
    permission_classes = ()
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password = password)

        if user:
            return Response({"token":user.auth_token.key})
        else:

            return Response({"error":"Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)