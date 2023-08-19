from django.shortcuts import render , redirect
from django.views import View
from .forms import BlogForm , PostForm , CategorieForm
from .models import Blog , Post
from django.views.generic import ListView , DetailView , UpdateView , DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Categories
from django.db.models import Q
from users.models import Profile


from hitcount.models import HitCount
from hitcount.views import HitCountDetailView
# Create your views here.


class CreateBlog(View):
    template_name = 'blog/create_blog.html'
    def get(self , request):
        try:
            user_has_blog = Blog.objects.get(user=request.user)
            if user_has_blog != None:
                return redirect('blog-management')
        except:
            pass

        form = BlogForm()
        context = {
            'form':form,
        }
        return render(request, self.template_name  , context)
    def post(self , request):
        form = BlogForm(request.POST , request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            user = request.user
            myform.user = user
            myform.save()
            return redirect('blog-management')
        context = {
            'form':form,
        }
        return render(request, self.template_name  , context)

class BlogManagement(View):
    def post(self,request):
        blog_user = Blog.objects.get(user=request.user)
        form = BlogForm(request.POST,request.FILES,instance=blog_user)
        # this form to update blog
        if form.is_valid():
            myform = form.save(commit=False)
            user =  request.user
            myform.user = user
            myform.save()
            return redirect('blog-management')
        # this form to submit post
        post_form = PostForm(request,request.POST , request.FILES )
        if post_form.is_valid():
            myform_post =  post_form.save(commit=False)
            myform_post.blog = blog_user
            myform_post.save()
            return redirect('blog-management')
        # add categorie to blog
        categorieform = CategorieForm(request.POST , request.FILES)
        if categorieform.is_valid():
            myform = categorieform.save(commit=False)
            myform.blog = blog_user
            myform.save()
            return redirect('blog-management')

        context = {
            'blog':blog_user,
            'form':form,
            'post_form':post_form,
            'categorieform':categorieform,
        }
        return render(request , 'blog/blog_management.html' , context)

    def get(self , request):
        blog_user = Blog.objects.get(user=request.user)
        form = BlogForm(instance=blog_user)
        posts_has_blog = Post.objects.all().filter(blog=blog_user)
        post_form = PostForm(request=request)
        categorieform = CategorieForm()
        # count views
        blog_posts = Post.objects.filter(blog__slug=blog_user)
        total_views = 0
        for post in blog_posts:
            hitcount = HitCount.objects.get_for_object(post)
            total_views += hitcount.hits
        context = {
            'blog':blog_user,
            'form':form,
            'post_form':post_form,
            'posts_has_blog':posts_has_blog,
            'total_views':total_views,
            'categorieform':categorieform,

        }
        return render(request , 'blog/blog_management.html' , context)

class PostEdit(View):
    def get(self,request,id):
        get_post = Post.objects.get(id=id)
        blog = Blog.objects.get(user=request.user)
        if blog == get_post.blog:
            form = PostForm(request,instance=get_post)
            context = {
                'blog':blog,
                'form':form,
            }
            return render(request , 'blog/post_edit.html' , context)
    def post(self,request,id):
        get_post = Post.objects.get(id=id)
        blog = Blog.objects.get(user=request.user)
        if blog == get_post.blog:
            form = PostForm(request,request.POST,request.FILES , instance=get_post)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.blog = blog
                myform.save()
                return redirect(f'/b/manage-blog/{id}/edit')

class PostsHasBlog(View):
    paginate_by = 2
    def get(self,request):
        blog_user = Blog.objects.get(user=request.user)
        posts_has_blog = Post.objects.all().filter(blog=blog_user)
        
        # start paginate
        queryset = posts_has_blog
        # create the paginator
        paginator = Paginator(queryset, self.paginate_by)
        # get the page number from the request
        page_number = self.request.GET.get('page')
        try:
            # get the page object
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # if the page is not an integer, return the first page
            page = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, raise a 404 error
            raise Http404
        page = page
        # end paginate


        context = {
            'page':page,
            'blog':blog_user,
        }
        return render(request, 'blog/posts_has_blog.html' , context)

class BlogView(View):
    paginate_by = 4
    def get(self , request ,slug ):
        get_blog = Blog.objects.get(slug=slug)
        posts = Post.objects.filter(blog=get_blog)
        post_2 = posts.order_by('-hit_count_generic__hits')[:2]
        post_4 = posts.order_by('-hit_count_generic__hits')[:4]
        post_5 = posts.order_by('-hit_count_generic__hits')[:5]
        template_name = get_blog.template
        author = Profile.objects.get(user=get_blog.user)
        # start paginate
        queryset = posts
        # create the paginator
        paginator = Paginator(queryset, self.paginate_by)
        # get the page number from the request
        page_number = self.request.GET.get('page')
        try:
            # get the page object
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # if the page is not an integer, return the first page
            page = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, raise a 404 error
            raise Http404
        page = page
        # end paginate
        context = {
            'page':page,
            'blog':get_blog,
            'post_2':post_2,
            'post_4':post_4,
            'post_5':post_5,
            'template_name':template_name,
            'author':author,
        }
        return render(request, f'blog/templates/{template_name}/{template_name}.html' , context)

class PostDetail(HitCountDetailView):
    model = Post
    template_name = 'blog/templates/nour/nour_detail.html'
    context_object_name = 'post'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = Blog.objects.get(slug=self.kwargs['blog'])
        author = Profile.objects.get(user=blog.user)
        context['author'] = author
        context['blog'] = blog
        post_4 = Post.objects.filter(blog=blog)[:4]
        context['post_4'] = post_4
        return context
    def queryset(self):
        return Post.objects.filter(id=self.kwargs['id'])
    def get_object(self, queryset=None):
        queryset = self.queryset() if queryset is None else queryset
        post_object = super().get_object(queryset)
        if post_object.blog.slug != self.kwargs['blog']:
            raise Http404("Post not found")
        return post_object

class SearchPage(View):
    def get(self ,request,slug ):
        query = request.GET['query']
        blog = Blog.objects.get(slug=slug)
        posts = Post.objects.filter(blog=blog)
        post_4 = posts.order_by('-hit_count_generic__hits')[:4]
        # start manage searching
        try:
            posts = Post.objects.filter(Q(title__icontains=query),blog=blog)[:10]
        except Post.DoesNotExist:
            try:
                posts = Post.objects.filter(Q(desc__icontains=query),blog=blog)[:10]
            except Post.DoesNotExist:
                try:
                    posts = Post.objects.filter(Q(content__icontains=query),blog=blog)[:10]
                except:
                    posts = None

        context = {
            'blog':blog,
            'post_4':post_4,
            'query':query,
            'posts':posts,
        }
        return render(request ,'blog/templates/nour/search.html' ,context)