from django.core import mail
connection = mail.get_connection()
import threading
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
# from rest_framework import status
# from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
from camera.models import Employee, Organization, Store, User, \
    Analytic, AnalyticDisplay, TotalDisplay, Client, \
    AnalyticEntry, TestUser, EmployeeMedia
from camera.permissions import IsOwnerOrReadOnly
from camera.serializers import EmployeeSerializer, \
    UserSerializer, OrganizationSerializer, StoreSerializer, \
    AnalyticSerializer, AnalyticDisplaySerializer, TotalDisplaySerializer, \
    ClientSerializer, AnalyticEntrySerializer, TestUserSerializer, EmployeeMediaSerializer

from camera.encode_faces import face_embedding



def index(request):
    return HttpResponse("Hello, world. You're at the dataviv index.")

##########################################################################


class OrganizationListCreate(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class OrganizationRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#############################################################################


# class TestUserListCreate(generics.ListCreateAPIView):
#     queryset = TestUser.objects.all()
#     serializer_class = TestUserSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# class TestUserRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TestUser.objects.all()
#     serializer_class = TestUserSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class TestUserListCreate(APIView):

    def get(self, request, format=None):

        print('in get list ------', request.query_params.get('pk', None))
        testuser = TestUser.objects.all()
        serializer = TestUserSerializer(testuser, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data=request.data
        print('data---',data.__dict__)
        t = TestUser.objects.create(media = data['media'])
        t.save()
        # serializer = TestUserSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Created"} )


class TestUserRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TestUser.objects.all()
    serializer_class = TestUserSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


##########################################################################


class EmployeeListCreate(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):

        print('in get list ------',request.query_params.get('pk', None))
        print('request user is -------------------------- ', self.request.user)
        # employee = Employee.objects.all()
        employee = Employee.objects.filter(owner=self.request.user).all()
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print('req data ----',request.data)
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            print(' store id is--', serializer.data['store'])
            print(' employee id is--', serializer.data['id'])
            print('employee media is--', serializer.data['employee_media'])
            # f = open("embedding/myfile.txt", "w")
            # f.write("Now the file has more content3!")
            # f.close()
            storage_path = "embedding"
            storeid = serializer.data['store']
            empid = serializer.data['id']
            video_file = serializer.data['employee_media']
            t1 = threading.Thread(target=face_embedding,args=([storage_path, storeid, empid, video_file,]),daemon=True)
            t1.start()
            # face_embedding(storage_path, storeid, empid, video_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
class EmployeeListCreate(APIView):
    # parser_classes = (JSONParser,)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    # parser_classes = (FileUploadParser,)


    def get(self, request, format=None):

        print('in get list ------',request.query_params.get('pk', None))
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print('req data ----', request.data)
        print('req data ----', request.FILES)
        try:
            data=request.data
            name=data['name']
            email=data['email']
            contact=data['contact']
            gender=data['gender']
            age=data['age']
            address=data['address']
            # employee_media=data['employee_media']
            employee_media=data.get('employee_media',False)
            store_id=data['store']

            store=Store.objects.get(id = store_id)
            ##############
            # print('data---',data.__dict__)
            # employee_id = data['employee']
            # print('employee_id-------------------',employee_id)
            # employee = Employee.objects.get(id = employee_id )
            # print('employee instance is -------------', employee)
            e = Employee.objects.create(
                name= name,
                email= email,
                contact= contact,
                gender= gender,
                age= age,
                address= address,
                employee_media = employee_media,
                store = store
                
                )

            e.save()

            # print('employee ------------------', e.employee_media)
            # print('employee details are ',e.id,e.store,e.employee_media)

            serializer = EmployeeSerializer(e)
            print('-----------*******************-----------------------',serializer.data)
            storage_path = "embedding"
            storeid = serializer.data['store']
            empid = serializer.data['id']
            video_file = serializer.data['employee_media']
            print('details to embedding -----',storeid,empid,video_file)
            t1 = threading.Thread(target=face_embedding,args=([storage_path, storeid, empid, video_file,]),daemon=True)
            t1.start()

            return Response({"message":"created"},status=status.HTTP_201_CREATED)
        except:
            return Response( {"message":"Error"},status=status.HTTP_400_BAD_REQUEST)

        


    # def post(self, request, format=None):
    #     print('req data ----',request.data)
    #     data=request.data
    #     print('data---',data.__dict__)
    #     if True:
    #         e = Employee.objects.create(
    #             name = data['name'],
    #             email = data['email'],
    #             contact=data['contact'],
    #             gender = data['gender'],
    #             age = data['age'],
    #             address = data['address'],
    #             employee_media = data['employee_media'],
    #             store = data['store']                    
    #             )
    #         e.save()
    #         # serializer = EmployeeSerializer(data=request.data)
    #         # if serializer.is_valid():
    #         #     serializer.save()
    #         #     print(' store id is--', serializer.data['store'])
    #         #     print(' employee id is--', serializer.data['id'])
    #         #     print('employee media is--', serializer.data['employee_media'])
    #         #     # f = open("embedding/myfile.txt", "w")
    #         #     # f.write("Now the file has more content3!")
    #         #     # f.close()
    #         storage_path = "embedding"
    #         storeid = e.store
    #         empid = e.id
    #         video_file = e.employee_media
    #         t1 = threading.Thread(target=face_embedding,args=([storage_path, storeid, empid, video_file,]),daemon=True)
    #         t1.start()
    #         # face_embedding(storage_path, storeid, empid, video_file)
    #         return Response( status=status.HTTP_201_CREATED)
    #     # except:
    #     else:
    #         return Response( status=status.HTTP_400_BAD_REQUEST)
'''
class EmployeeRetriveUpdateDestroy(APIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print('pk-------------',pk)
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

###################################################################################

# class EmployeeListCreate(generics.ListCreateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer


# class EmployeeRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

##########################################################################
class EmployeeMediaListCreate(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):

        print('in get list ------',request.query_params.get('pk', None))
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print('req data ----',request.data)
        data=request.data
        print('data---',data.__dict__)
        employee_id = data['employee']
        print('employee_id-------------------',employee_id)
        employee = Employee.objects.get(id = employee_id )
        print('employee instance is -------------', employee)
        em = EmployeeMedia.objects.create(employee_media = data['employee_media'], employee = employee)
        em.save()
        serializer = EmployeeMediaSerializer(em)
        print('-----------*******************-----------------------',serializer.data)
        storage_path = "embedding"
        storeid = 1
        empid = serializer.data['employee']
        video_file = serializer.data['employee_media']
        t1 = threading.Thread(target=face_embedding,args=([storage_path, storeid, empid, video_file,]),daemon=True)
        t1.start()
        # face_embedding(storage_path, storeid, empid, video_file)
        # serializer = EmployeeSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "created successfully"})


##########################################################################
class StoreListCreate(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

#####

##########################################################################


class AnalyticListCreate(generics.ListCreateAPIView):
    queryset = Analytic.objects.all()
    serializer_class = AnalyticSerializer


class AnalyticRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Analytic.objects.all()
    serializer_class = AnalyticSerializer


##########################################################################
class AnalyticDisplayListCreate(generics.ListCreateAPIView):
    queryset = AnalyticDisplay.objects.all()
    serializer_class = AnalyticDisplaySerializer


class AnalyticDisplayRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnalyticDisplay.objects.all()
    serializer_class = AnalyticDisplaySerializer

#########################################################################


class TotalDisplayListCreate(generics.ListCreateAPIView):
    queryset = TotalDisplay.objects.all()
    serializer_class = TotalDisplaySerializer


class TotalDisplayRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TotalDisplay.objects.all()
    serializer_class = TotalDisplaySerializer

#########################################################################
#########################################################################


class ClientListCreate(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):

        print('in get list ------', request.query_params.get('pk', None))
        client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientRetriveUpdateDestroy(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print('pk-------------',pk)
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#########################################################################
##########################################################################
# ############$$$$$$$$$$$$$$$$$$$$$$$$$$$$#################################
#########################################################################


class AnalyticEntryListCreate(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):

        print('in get list ------', request.query_params.get('pk', None))
        analyticentry = AnalyticEntry.objects.all()
        serializer = AnalyticEntrySerializer(analyticentry, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AnalyticEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyticEntryRetriveUpdateDestroy(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return AnalyticEntry.objects.get(pk=pk)
        except AnalyticEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print('pk-------------',pk)
        analyticentry = self.get_object(pk)
        serializer = AnalyticEntrySerializer(analyticentry)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        analyticentry = self.get_object(pk)
        serializer = AnalyticEntrySerializer(analyticentry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        analyticentry = self.get_object(pk)
        serializer = AnalyticEntrySerializer(analyticentry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        analyticentry = self.get_object(pk)
        analyticentry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#########################################################################
# ############$$$$$$$$$$$$$$$$$$$$$$$$$$$$$################################


class UserCreate(generics.CreateAPIView):
    # parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        print('request.data----------',request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print('balfdfffffffffffffffffffffffffffff',serializer.instance)
        # user = serializer.data['username']
        # user = User.objects.get(pk=pk_of_user_without_token)
        token = Token.objects.create(user=serializer.instance)
        print('token---------------------', token)
        print('serializer.data in UserCreate in create defn is-', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailView2(APIView):
    permission_classes = ()

    def post(self, request,):
        pk = request.data.get("pk")
        print('id is ------------',pk)
        employee = Employee.objects.get(pk=pk)
        print('employee----',employee)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

###################################################################

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'token':reset_password_token.key,
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('camera/user_reset_password.html', context)
    email_plaintext_message = render_to_string('camera/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
