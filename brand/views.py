from openai import OpenAI

import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import BrandForm
from .models import Brand
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Load environment variables if using python-dotenv
from dotenv import load_dotenv
load_dotenv()

# Ensure the API key is set correctly
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise Exception("OPENAI_API_KEY environment variable is not set.")
client = OpenAI(api_key=api_key)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'brand/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

@login_required
def home(request):
    return render(request, 'brand/home.html')

@login_required
def create_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.user = request.user
            brand.save()
            return redirect('home')
    else:
        form = BrandForm()
    return render(request, 'brand/create_brand.html', {'form': form})

@login_required
@csrf_exempt
def chatbot(request):
    conversation = []
    if request.method == 'POST':
        user_input = json.loads(request.body).get('user_input')
        brand_info = get_brand_info(request.user)

        # Define the API request parameters
        completion_params = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"User question: {user_input}\nBrand information: {brand_info}"}
            ]
        }

        try:
            response = client.chat.completions.create(**completion_params)
            answer = response.choices[0].message.content.strip()
            conversation.append({"role": "user", "content": user_input})
            conversation.append({"role": "AI", "content": answer})
            return JsonResponse({"answer": answer})
        except Exception as e:  # Catching the base Exception class
            error_message = str(e)
            return JsonResponse({"error_message": error_message})

    return render(request, 'brand/chatbot.html', {'conversation': conversation})

def get_brand_info(user):
    brand = Brand.objects.filter(user=user).first()
    if brand:
        return f"Name: {brand.name}, Description: {brand.description}, Q1: {brand.question_1}, Q2: {brand.question_2}"
    return "No brand information available."
