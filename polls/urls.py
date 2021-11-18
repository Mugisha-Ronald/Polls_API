from django.urls import path
# from .views import polls_list, polls_detail



# urlpatterns = [
#     path("polls/",polls_list,name= "polls_list"),
#     path("polls/<int:pk>/", polls_detail,name="polls_detail")
# ]


""" after creating the serializers (to serialize and derialize our data), and  the APIView lists, we change our urls to the following"""

from .apiviews import PollList , PollDetail , ChoiceList , CreateVote,UserCreate,LoginView

# urlpatterns = [
#     path("polls/",PollList.as_view(),name= "polls_list"),
#     path("polls/<int:pk>/", PollDetail.as_view(),name="polls_detail"),
#     path("choices/",ChoiceList.as_view(), name= "choice_list"),
#     path("vote/",CreateVote.as_view(), name = "create_vote")
# ]

"""
After changing our apivies basically the ChoiceList and CreateVote; we need to change our urls to a nested 
structure as below
"""

urlpatterns = [
    path("users/",UserCreate.as_view(),name="user_create"),
    path("login/",LoginView.as_view(), name="login"),
    path("polls/",PollList.as_view(),name= "polls_list"),
    path("polls/<int:pk>/", PollDetail.as_view(),name="polls_detail"),
    path("polls/<int:pk>/choices", ChoiceList.as_view(),name="choice_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/",CreateVote.as_view(), name= "create_vote"),
]

# You can see the changes by doing a GET to http://localhost:8000/polls/1/choices/
# You can vote for choices 2, of poll 1 by doing a POST to http://localhost:8000/polls/1/choices/2/vote/ 
#with data {"voted_by": 1}.

# Introducing Viewsets and routers

from rest_framework.routers import DefaultRouter
from .apiviews import PollViewSet


router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls')

urlpatterns += router.urls
