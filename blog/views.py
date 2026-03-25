from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages


# ---------------- HOME ----------------
def home(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'blog/home.html', {'posts': posts, 'categories': categories})
    else:
        return render(request, 'blog/home.html', {'categories': categories})

# ---------------- DÉTAIL POST ----------------
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    categories = Category.objects.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'categories': categories})

# ---------------- POSTS PAR CATÉGORIE ----------------
def category_posts(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blog/category_posts.html', {'posts': posts, 'category': category, 'categories': categories})

# ---------------- MES ARTICLES ----------------
@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blog/my_posts.html', {'posts': posts, 'categories': categories})

# ---------------- AJOUTER POST ----------------
@login_required
def add_post(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']
        category = get_object_or_404(Category, pk=category_id)
        
        # ✅ récupérer l'image
        image = request.FILES.get('image')  # None si pas d'image
        
        Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            category=category,
            image=image
        )
        messages.success(request, 'Article ajouté avec succès !')
        return redirect('home')
    return render(request, 'blog/add_post.html', {'categories': categories})

# ---------------- ÉDITER POST ----------------
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Sécurité : seul l'auteur ou superuser peut modifier
    if request.user != post.author and not request.user.is_superuser:
        messages.error(request, "Vous ne pouvez pas modifier cet article.")
        return redirect('home')

    categories = Category.objects.all()

    

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')

        category_id = request.POST.get('category')
        if category_id:
            post.category = get_object_or_404(Category, pk=category_id)
            
        
        if 'image' in request.FILES:
            post.image = request.FILES['image']

        post.save()

        messages.success(request, "Article modifié avec succès !")
        return redirect('post_detail', post_id=post.id)

    return render(request, 'blog/edit_post.html', {
        'post': post,
        'categories': categories
    })
    
# ---------------- SUPPRIMER POST ----------------
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author and not request.user.is_superuser:
        messages.error(request, "Vous ne pouvez pas supprimer ce post.")
        return redirect('home')
    post.delete()
    messages.success(request, 'Article supprimé avec succès !')
    return redirect('home')

# ---------------- INSCRIPTION ----------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # Supprimer help_text avant validation
        form.fields['username'].help_text = ''
        form.fields['password1'].help_text = ''
        form.fields['password2'].help_text = ''

        if form.is_valid():
            user = form.save()
            login(request, user)  # connexion automatique après inscription
            messages.success(request, f"Bienvenue {user.username} ! Vous êtes connecté.")
            return redirect('home')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserCreationForm()
        # Supprimer help_text pour l'affichage initial
        form.fields['username'].help_text = ''
        form.fields['password1'].help_text = ''
        form.fields['password2'].help_text = ''

    return render(request, 'blog/register.html', {'form': form})

# ---------------- ADMIN DASHBOARD ----------------
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    categories = Category.objects.all()
    return render(request, 'blog/admin_dashboard.html', {
        'total_users': total_users,
        'total_posts': total_posts,
        'categories': categories
    })

# ---------------- ADMIN GESTION CATÉGORIES ----------------
@login_required
def admin_categories(request):
    if not request.user.is_superuser:
        return redirect('home')
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name)
        return redirect('admin_categories')
    return render(request, 'blog/admin_categories.html', {'categories': categories})

@login_required
def delete_category(request, category_id):
    if not request.user.is_superuser:
        return redirect('home')
    cat = get_object_or_404(Category, pk=category_id)
    cat.delete()
    return redirect('admin_categories')

# ---------------- ADMIN GESTION UTILISATEURS ----------------
@login_required
def admin_users(request):
    if not request.user.is_superuser:
        return redirect('home')
    users = User.objects.all()
    return render(request, 'blog/admin_users.html', {'users': users})

@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')
    user = get_object_or_404(User, pk=user_id)
    if user.is_superuser:
        messages.error(request, "Vous ne pouvez pas supprimer un super utilisateur !")
        return redirect('admin_users')
    user.delete()
    return redirect('admin_users')
#--------------deconnexion------------------
def logout_view(request):
    logout(request)          # déconnecte l'utilisateur
    request.session.flush()  # vide complètement la session
    messages.success(request, "Vous êtes bien déconnecté.")
    return redirect('home')