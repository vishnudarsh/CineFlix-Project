from django.shortcuts import render,redirect

from django.views import View

from .models import Movie,IndustryChoices,GenereChoices,ArtistChoices,LanguageChoices,CertificationChoices

from .forms import MovieForm

from django.db.models import Q 

from django.utils.decorators import method_decorator

from authentication.permissions import permitted_user_roles


# Create your views here.



class HomeView(View):

        template = 'home.html'


        def get(self,request,*args,**kawargs):


          data ={'page':'Home'}

          return render (request,self.template,context= data)

class MovieListView(View):

    template = 'movies/movie-list.html'

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')

        movies=Movie.objects.filter(active_status = True)

        if query :

            movies = movies.filter(Q(name__icontains=query) |
                                   Q(description__icontains=query) |
                                   Q(industry_name_icontains=query) |
                                   Q(certification__icontains=query) |
                                   Q(genere_name_icontains=query) |
                                   Q(artist_name_icontains=query) |
                                   Q(languages_name_icontains=query) |
                                   Q(tags__icontains=query)
                                   ).distinct()

        data={'page':'Movies','movies':movies,'query':query}

        return render(request,self.template,context=data)
    
# class MovieCreateView(View):

#     def get(self, request, *args, **kwargs):

#         industry_choices = IndustryChoices
#         genere_choices =GenereChoices
#         language_choices =LanguageChoices
#         artist_choices =ArtistChoices
#         certification_choices =CertificationChoices

#         data ={'page':'Create Movies',
#                 'industry_choices':industry_choices,
#                 'genere_choices':genere_choices,
#                 'language_choices' :language_choices,
#                 'artist_choices' :artist_choices,
#                 'certification_choices' :certification_choices
#                 }

#         return render(request, 'movies/movie-create.html',context=data)  
    
#     def post(self, request, *args, **kwargs):

#         movie_data = request.POST

#         name = movie_data.get('name')

#         photo = request.FILES.get('photo')

#         description = movie_data.get('description')

#         release_date = movie_data.get('release_date')

#         runtime = movie_data.get('runtime')

#         industry = movie_data.get('industry')

#         genere = movie_data.get('genere')

#         artist = movie_data.get('artist')

#         video = movie_data.get('video')

#         tags = movie_data.get('tags')

#         languages = movie_data.get('languages')

#         #to create db

#         Movie.objects.create(name=name,
                             
#                              photo=photo,
                             
#                              description = description,

#                              release_date = release_date,

#                              industry = industry,

#                              runtime = runtime,

#                              languages = languages,

#                              artist = artist,

#                              genere = genere,

#                              video = video,

#                              tags = tags,
                             
#                              )

#         return redirect('movie-list')
    
@method_decorator(permitted_user_roles(['Admin']),name='dispatch')

class MovieCreateView(View):

    form_class = MovieForm

    template = 'movies/movie-create.html'

    def get(self, request, *args, **kwargs):

        form = self.form_class()

        form = MovieForm()

        data ={'page':'Create Movies',
               
               'form':form
          
                }

        return render(request,self.template ,context=data)  
    
    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST,request.FILES)

        

        if form.is_valid():

            form.save()

            return redirect('movie-list')    
        

        data ={'form':form,'page':'Create Movie '}

        return render(request, self.template,context=data) 
    
# class MovieDetailsView(View):               (implimenting with id)

#     template = 'movies/movie-details.html'

#     def get(self, request, *args, **kwargs):

#         id = kwargs.get('id')

#         movie = Movie.objects.get(id=id)

#         data = {'movie':movie,'page':movie.name}

#         return render(request,self.template,context=data)

class MovieDetailsView(View):

    template = 'movies/movie-details.html'

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        data = {'movie':movie,'page':movie.name}

        return render(request,self.template,context=data)
    
@method_decorator(permitted_user_roles(['Admin']),name='dispatch')    
class MovieEditView(View):

    form_class = MovieForm

    template = 'movies/movie-edit.html'

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        form = self.form_class(instance=movie)

        data = {'form':form,'page':movie.name}

        return render(request,self.template,context=data)
    
    def post(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        form =self.form_class(request.POST, request.FILES, instance=movie)

        if form.is_valid():

            form.save()

            return redirect ('movie-details', uuid=uuid)
        
        data = {'form':form,'page':movie.name}

        return render(request,self.template,context=data)

@method_decorator(permitted_user_roles(['Admin']),name='dispatch')
class MovieDeleteView(View):

    def get(self, request, *args, **kwargs):

         uuid = kwargs.get('uuid')

         movie = Movie.objects.get(uuid=uuid)

        #  hard delete
        #  movie.delete()    
        # soft delete
         movie.active_status = False

         movie.save()

         return redirect ('movie-list')