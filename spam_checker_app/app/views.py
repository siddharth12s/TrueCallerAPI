from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import User, Contacts, SpamNumber
from app.serializers import UserSerializer, ContactSerializer, SpamNumberSerializer

# Create your views here.
# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class LoginView(APIView):

    permission_classes = [AllowAny]
    
    def post(self,request):
        phone_no = request.data.get('phone_no')
        password = request.data.get('password')
        
        if phone_no is None or password is None:
            return Response({"message": "Please enter correct credentials"})
        
        user = User.objects.filter(phone_no=phone_no).first()
        
        if user is None:
            return Response({"error": "User does not exist"})
        
        if not user.check_password(password):
            return Response({"error": "User password is incorrect"})
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return Response({"access_token": access_token, "refresh_token": refresh_token})


class ContactsViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        print("user is", self.request.user)
        queryset = Contacts.objects.filter(user=self.request.user) 
        return queryset
    


class MarkUnmarkSpam(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action, spam_number, *args, **kwargs):
        if action == 'mark':
            return self.mark_spam(request, spam_number)
        elif action == 'unmark':
            return self.unmark_spam(request, spam_number)
        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

    def mark_spam(self, request, spam_number):
        try:
            spam_obj = SpamNumber.objects.get(spam_number=spam_number, user=request.user)
            return Response({'detail': 'Number is already marked as spam.'}, status=status.HTTP_400_BAD_REQUEST)
        except SpamNumber.DoesNotExist:
            spam_obj = SpamNumber(spam_number=spam_number, user=request.user)
            spam_obj.save()
            return Response({'detail': 'Number marked as spam.'}, status=status.HTTP_201_CREATED)

    def unmark_spam(self, request, spam_number):
        try:
            spam_obj = SpamNumber.objects.get(spam_number=spam_number, user=request.user)
            spam_obj.delete()
            return Response({'detail': 'Number unmarked from spam.'}, status=status.HTTP_204_NO_CONTENT)
        except SpamNumber.DoesNotExist:
            return Response({'detail': 'Number is not in the spam list.'}, status=status.HTTP_404_NOT_FOUND)



class Search(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search_type = request.query_params.get('type', '')
        search_query = request.query_params.get('q', '')

        if search_type == 'name':
            return self.search_by_name(request, search_query)
        elif search_type == 'phone':
            return self.search_by_phone(request, search_query)
        else:
            return Response({'detail': 'Invalid search type.'}, status=status.HTTP_400_BAD_REQUEST)

    def search_by_name(self, request, search_query):
        start_with_results = Contacts.objects.filter(contact_name__istartswith=search_query)
        contain_results = Contacts.objects.filter(contact_name__icontains=search_query).exclude(contact_name__istartswith=search_query)
        
        all_results = list(start_with_results) + list(contain_results)
        
        data_list = []
        for result in all_results:
            is_spam = SpamNumber.objects.filter(spam_number=result.contact_number).exists()
            serializer = ContactSerializer(result)
            result_data = serializer.data
            result_data['is_spam'] = is_spam
            data_list.append(result_data)
        
        return Response(data_list, status=status.HTTP_200_OK)

    def search_by_phone(self, request, search_query):
        registered_user_result = Contacts.objects.filter(contact_number=search_query, user__isnull=False)
        is_spam = SpamNumber.objects.filter(spam_number=search_query).exists()

        if registered_user_result.exists():
            serializer = ContactSerializer(registered_user_result.first())
            data = serializer.data
            data['is_spam'] = is_spam
            return Response(data, status=status.HTTP_200_OK)

        all_results = Contacts.objects.filter(contact_number=search_query)
        serializer = ContactSerializer(all_results, many=True)

        data_list = []
        for result in serializer.data:
            result['is_spam'] = is_spam
            data_list.append(result)

        return Response(data_list, status=status.HTTP_200_OK)
