from random import choice
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *
import json
import datetime
from .forms import SignUpForm, QuestionForm, AnswerForm, ChallengeAnswerForm
from .utils import cookieCart, cartData

def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login concluído!")
            return redirect('home')
        else:
            messages.success(request, "Não foi possível concluir o login.")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def signup_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(request, username=username, password=password)
			login(request, user)
			messages.success(request, "Bem-vindo(a)!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'signup.html', {'form':form})

	return render(request, 'signup.html', {'form':form})


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    category_id = request.GET.get('category')
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'store.html', {'products' : products, 'cartItems': cartItems, 'categories': categories})


@login_required
def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']          
        
    return render(request, 'cart.html', {'items': items, 'order': order, 'cartItems': cartItems})

@login_required
def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    return render(request, 'checkout.html', {'items': items, 'order': order, 'cartItems': cartItems})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        Address.objects.create(
            user = user,
            order = order,
            street = data['shipping']['street'],
            city = data['shipping']['city'],
            postal_code = data['shipping']['postal_code'],
        )

    else:
        print('User is not logged in')

        print('COOKIES:', request.COOKIES)
        name = data['form']['username']
        email = data['form']['password']

        cookieData = cookieCart(request)
        items = cookieData['items']

        

    return JsonResponse('Payment complete', safe=False)

@login_required
def forum(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user  # Assign the current user to the question
            question.save()
            return redirect('forum')  # Redirect to the forum page after successfully creating the question
    else:
        form = QuestionForm()
    
    return render(request, 'forum.html', {'questions': questions, 'form': form})

@login_required
def question(request, id):
    question = Question.objects.get(pk=id)
    answers = Answer.objects.filter(question=question)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user  # Assign the current user to the answer
            answer.question = question
            answer.save()
            return redirect('question', id=id)  # Redirect back to the same question page after submitting the answer
    else:
        form = AnswerForm()

    return render(request, 'question.html', {'question': question, 'answers': answers, 'form': form})

@login_required
def challenge(request):
    current_date = datetime.date.today()

    # Check if a session variable for the selected challenge exists
    selected_challenge_id = request.session.get('selected_challenge_id')

    # If a session variable is not set or the challenge doesn't match the date, select a challenge
    if not selected_challenge_id:
        # Filter challenges for the current date
        challenges = Challenge.objects.filter(date=current_date)

        if challenges:
            # Choose a random challenge from the list
            selected_challenge = choice(challenges)
            # Store the selected challenge's ID in the session
            request.session['selected_challenge_id'] = selected_challenge.id
        else:
            selected_challenge = None
    else:
        try:
            # Retrieve the challenge from the session variable
            selected_challenge = Challenge.objects.get(pk=selected_challenge_id)
        except Challenge.DoesNotExist:
            selected_challenge = None

    if request.method == 'POST':
        form = ChallengeAnswerForm(request.POST)
    else:
        form = ChallengeAnswerForm()


    return render(request, 'challenge.html', {'challenge': selected_challenge, 'form': form})
