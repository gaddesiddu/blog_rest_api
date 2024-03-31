from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes

from rest_framework.response import Response
from .models import CustomUser  # Import your CustomUser model
from .serializers import UserSerializer, ParagraphSerializer # Import your UserSerializer
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count
from .models import Word, Paragraph
import re

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def search_paragraphs(request, word):
    # Converted the search word to lowercase
    search_word = word.lower()

    # Query the Paragraph model to get all paragraphs
    all_paragraphs = Paragraph.objects.all()

    # Initialize a list to hold the matching paragraph(s)
    matching_paragraphs = []

    # Iterate through paragraphs to find the exact match
    for paragraph in all_paragraphs:
        # Tokenize the paragraph text
        words = paragraph.text.split()
        words_lower = [word.lower() for word in words]

        # Check if the search word is in the paragraph
        if search_word in words_lower:
            matching_paragraphs.append(paragraph)

    # Serialize the matching paragraph data
    serializer = ParagraphSerializer(matching_paragraphs, many=True)

    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def post_data(request):
    # Extract paragraph from request data
    paragraph_text = request.data.get('paragraph')

    # Check if paragraph text is provided
    if not paragraph_text:
        return Response({'error': 'Paragraph text is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Tokenize words by splitting at whitespace
    words = paragraph_text.split()

    # Convert all words to lowercase
    words_lower = [word.lower() for word in words]

    # Generate a unique ID for the paragraph
    # You can use Django's auto-generated primary key for this purpose
    # Alternatively, can generate a UUID
    # For simplicity, let's assume  using the auto-generated primary key
    # In this case, we can leave it blank and let the database handle it

    # Identify paragraphs based on two newline characters
    paragraphs = re.split(r'\n{2,}', paragraph_text.strip())

    # Create a Paragraph instance for each identified paragraph
    paragraphs_data = []
    for idx, paragraph_text in enumerate(paragraphs, start=1):
        paragraph = Paragraph.objects.create(text=paragraph_text)
        paragraphs_data.append({'id': paragraph.id, 'text': paragraph_text})

        # Index words against the paragraph they are from
        for word in words_lower:
            Word.objects.create(word=word, paragraph=paragraph)

    return Response(paragraphs_data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])  # Add JWT authentication
def update_data(request, pk):
    user_obj = CustomUser.objects.get(pk=pk)  # Fetch the existing user object
    serializer = UserSerializer(user_obj, data=request.data, partial=True)  # Use partial=True to allow partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])  # Add JWT authentication
def delete_data(request, pk):
    user_obj = CustomUser.objects.get(pk=pk)
    user_obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
