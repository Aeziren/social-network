import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follow

ITEMS_PER_PAGE = 10

def index(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            new_post = Post(user=request.user, content=content)
            new_post.save()

    posts = Post.objects.all().order_by("-timestamp")


    liked_posts = []
    if request.user.is_authenticated:
        for item in request.user.liked.all():
            liked_posts.append(item.post)

    # Pagination
    pages = Paginator(posts, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = pages.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def user(request, username):
    profile = User.objects.get(username=username)
    posts = Post.objects.filter(user=profile)
    qtt_following = profile.following.count()
    qtt_followers = profile.followers.count()

    same_user = request.user == profile
    following = False
    if not same_user and request.user.is_authenticated:
        following = Follow.objects.filter(from_user=request.user, to_user=profile).exists()

    liked_posts = []
    if request.user.is_authenticated:
        for item in request.user.liked.all():
            liked_posts.append(item.post)

    # Pagination
    pages = Paginator(posts, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = pages.get_page(page_number)

    return render(request, "network/user.html", {
        "profile": profile,
        "qtt_following": qtt_following,
        "qtt_followers": qtt_followers,
        "qtt_posts": posts.count(),
        "page_obj": page_obj,
        "same_user": same_user,
        "following": following,
        "follow_type": "unfollow" if following else "follow",
        "liked_posts": liked_posts
    })

@login_required
@csrf_exempt
def follow_toggle(request):
    if request.method == "POST":
        data = json.loads(request.body)

        follow_type = data.get("follow_type")
        from_user = User.objects.get(username=data.get("from_user"))
        to_user = User.objects.get(username=data.get("to_user"))

        if follow_type == "follow":
            new_following = Follow(from_user=from_user, to_user=to_user)
            new_following.save()
        else:
            following = Follow.objects.get(from_user=from_user, to_user=to_user)
            following.delete()

        return JsonResponse({"message": "Success!"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def following(request):
    # Get list of follow relationships
    follow_list = Follow.objects.filter(from_user=request.user)

    # Create a list of posts based on followed users
    posts = []
    for item in follow_list:
        posts.extend(Post.objects.filter(user=item.to_user))

    liked_posts = []
    if request.user.is_authenticated:
        for item in request.user.liked.all():
            liked_posts.append(item.post)

    # Pagination
    pages = Paginator(posts, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = pages.get_page(page_number)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })

@csrf_exempt
@login_required
def edit(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except:
        return JsonResponse({"message": "Post not found"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        changes = data.get("changes")

        post.content = changes
        post.save()

        return JsonResponse({"message": "Sucess"}, status=200)

    return JsonResponse({"message": "Invalid method"}, status=405)

@csrf_exempt
@login_required
def toggle_like(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)

        if not request.user.is_authenticated:
            return JsonResponse({"message": "Authentication required"}, status=403)

        # Check whether is like or unlike request
        action = data.get("action")

        post = Post.objects.get(pk=post_id)

        if action == "like":
            # Create new like entry
            new_like = Like(user=request.user, post=post)
            new_like.save()

            #Update like counter on post
            post.qtt_likes += 1
        elif action == "unlike":
            # Remove like entry
            like = Like.objects.get(user=request.user, post=post)
            like.delete()

            #Update like counter on post
            post.qtt_likes -= 1
        #Save changes on post
        post.save()

        return JsonResponse({"message": "Success"}, status=200)

    else:
        return JsonResponse({"message": "Invalid method"}, status=405)



