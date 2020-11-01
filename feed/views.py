from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import *
from django.views.generic import ListView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

def home(request):
    posts = Post.objects.filter(is_active=True)
    cates = Category.objects.filter(is_active=True)
    context = {
        'posts':posts,
        'cates':cates
    }
    return render(request, 'feed/index.html', context)

class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        art = Art.objects.filter(category=category, is_active=True)
        context = {
            'object_list': art,
            'category_title': category,
            'category_description': category.description,
            'category_image': category.image
        }
        return render(self.request, "feed/category-details.html", context)
        
class ArtListView(ListView):
	model = Art
	template_name = 'feed/gallery.html'
	context_object_name = 'arts'
	ordering = ['-created_on']
	paginate_by = 10
	def get_context_data(self, **kwargs):
		context = super(ArtListView, self).get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			liked = [i for i in Art.objects.all() if Like.objects.filter(user = self.request.user, art=i)]
			context['liked_art'] = liked
			posts = Post.objects.all()
			context['posts'] = posts
			cates = Category.objects.filter(is_active=True)
			context['cates'] = cates
		return context

class UserArtListView(LoginRequiredMixin, ListView):
	model = Art
	template_name = 'feed/user_arts.html'
	context_object_name = 'arts'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(UserArtListView, self).get_context_data(**kwargs)
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		liked = [i for i in Art.objects.filter(user_name=user) if Like.objects.filter(user = self.request.user, art=i)]
		context['liked_art'] = liked
		return context

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Art.objects.filter(user_name=user).order_by('-created_on')


@login_required
def art_detail(request, pk):
	art = get_object_or_404(Art, pk=pk)
	user = request.user
	is_liked =  Like.objects.filter(user=user, art=art)
	if request.method == 'POST':
		form = NewCommentForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)
			data.art = art
			data.username = user
			data.save()
			return redirect('art-detail', pk=pk)
	else:
		form = NewCommentForm()
	return render(request, 'feed/art_detail.html', {'art':art, 'is_liked':is_liked, 'form':form})
	
@login_required
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	user = request.user
# 	is_liked =  Like.objects.filter(user=user, post=post)
	if request.method == 'POST':
		form = NewCommentpostForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)
			data.post = post
			data.username = user
			data.save()
			return redirect('post-detail', pk=pk)
	else:
		form = NewCommentForm()
	return render(request, 'feed/post_detail.html', {'post':post, 'form':form})

@login_required
def create_art(request):
	user = request.user
	if request.method == "POST":
		form = NewArtForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.save(commit=False)
			data.user_name = user
			data.save()
			messages.success(request, f'Posted Successfully')
			return redirect('home')
	else:
		form = NewArtForm()
	return render(request, 'feed/create_art.html', {'form':form})

class ArtUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Art
	fields = ['title','description', 'pic', 'tags', 'category']
	template_name = 'feed/create_art.html'

	def form_valid(self, form):
		form.instance.user_name = self.request.user
		return super().form_valid(form)

	def test_func(self):
		art = self.get_object()
		if self.request.user == art.user_name:
			return True
		return False

class ArtDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Art
	success_url = '/'

	def test_func(self):
		art = self.get_object()
		if self.request.user == art.user_name:
			return True
		return False

@login_required
def search_arts(request):
	query = request.GET.get('p')
	object_list = Art.objects.filter(tags__icontains=query)
	liked = [i for i in object_list if Like.objects.filter(user = request.user, art=i)]
	context ={
		'arts': object_list,
		'liked_art': liked
	}
	return render(request, "feed/search_posts.html", context)

@login_required
def like(request):
	art_id = request.GET.get("likeId", "")
	user = request.user
	art = Art.objects.get(pk=art_id)
	liked= False
	like = Like.objects.filter(user=user, art=art)
	if like:
		like.delete()
	else:
		liked = True
		Like.objects.create(user=user, art=art)
	resp = {
        'liked':liked
    }
	response = json.dumps(resp)
	return HttpResponse(response, content_type = "application/json")






