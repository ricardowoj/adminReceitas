from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro(request):
    """Cadastra uma nova pessoa no sistema."""
    if request.method == "POST":
        nome = request.POST["nome"]
        email = request.POST["email"]
        senha = request.POST["password"]
        senha_confirmacao = request.POST["password2"]
        if not nome.strip():
            return redirect("cadastro")
        if not email.strip():
            return redirect("cadastro")
        if senha != senha_confirmacao:
            messages.error(request, "As senhas não são iguais!")
            return redirect("cadastro")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Faça login, e-mail já existe!")
            return redirect("login")
        if User.objects.filter(username=nome).exists():
            messages.error(request, "Nome já consta cadastrado!")
            return redirect("cadastro")
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect("login")
    else:
        return render(request, "usuarios/cadastro.html")


def login(request):
    """Realiza o login da pessoa no sistema."""
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]
        if email == "" and senha == "":
            messages.warning(request, "Insira o e-mail para realizar login!")
            messages.warning(request, "Insira a senha para realizar login!")
            return redirect("login")

        if email == "":
            messages.warning(request, "Insira o e-mail para realizar login!")
            return redirect("login")

        if senha == "":
            messages.warning(request, "Insira a senha para realizar login!")
            return redirect("login")

        if User.objects.filter(email=email).exists():
            nome = (
                User.objects.filter(email=email)
                .values_list("username", flat=True)
                .get()
            )
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    else:
        return render(request, "usuarios/login.html")


def logout(request):
    """Deslogar a pessoa do sistema."""
    auth.logout(request)
    return redirect("index")


def dashboard(request):
    """Apresentar as receitas somente da pessoa logada."""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by("-date_receita").filter(pessoa=id)
        dados = {"receitas": receitas}
        return render(request, "usuarios/dashboard.html", dados)
    else:
        return redirect("index")
