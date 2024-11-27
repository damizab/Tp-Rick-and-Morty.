# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages()
    if request.user.is_authenticated:
        favourite_list = services.getAllFavourites
    else:
        favourite_list =[]       
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', '')
    if (search_msg != ''):
        images = services.getAllImages(search_msg)
        favourite_list= []
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list})        
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    favourite= services.getAllFavourites(request)
    for favorito in favourite:
        favourite_list.append(favorito)
    return render(request, 'favourites.html', {'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    favourite_list = services.getAllFavourites(request)
    image= services.getAllImages()
    return render(request,'home.html', {'images': image,'favourite.html': favourite_list})
    
@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    favourite_list = services.getAllFavourites(request)
    
    return render(request,'favourites.html', {'favourite_list': favourite_list })

@login_required
def exit(request):
    logout(request)
    return render( request, 'index.html')