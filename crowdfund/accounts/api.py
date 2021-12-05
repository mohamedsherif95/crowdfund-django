from knox.models import AuthToken 
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
# from knox.views import LoginView as KnoxLoginView
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import UserSerializer, RegisterSerializer, LoginUserSerializer
from django.contrib.auth import login


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        # domain = get_current_site(request).domain
        # link = reverse('accounts:activate', kwargs={
        #             'uidb64': uidb64, 'token': token_generator.make_token(user)})

        # activate_url = f'http://{domain}{link}'
                
        # email_body = f'Here is your activation link:\n{activate_url}'

        # send_mail(
        #         'Account Activation Email',
        #         email_body,
        #         'noreply@semicolon.com',
        #         [user.email],
        #         fail_silently=False,
        #         )
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        # "activate url": activate_url
        })
        
# Login API   
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })   
        
   
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user        