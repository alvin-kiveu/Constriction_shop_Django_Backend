from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        print(f"Email: {email}, Password: {password}")

        user = User.objects.filter(email = email).first()

        if user is None:
            raise AuthenticationFailed('user not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')



        response =  Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'jwt': token
        }
        return response




