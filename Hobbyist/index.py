####### This is the code snippets for a django project I was working on with Prosper IT consulting. This code utilizes a
gui that can add guitars to a collection for a collector to keep a record of his guitars. I also utilizing customized styling
which can be seen in the CSS files at the bottom. ############






##### VIEWS #####

from django.shortcuts import render, redirect, get_object_or_404
from .models import Guitar          #import the class of Guitar to be able to use object definition
from .forms import GuitarForm       #import the Guitar Form to be able to create and save
from .api_service import *          #imports the functions from the API Service module created



# renders home page for the JimiJams app

def jimiAdmin(request):
    return render(request, 'JimiJams/JimiJams_home.html')

#View function that controls the main index page - list of jerseys
def guitarList(request):
    get_guitars = Guitar.Guitars.all()      #Gets all the current jerseys from the database
    context = {'guitars': get_guitars}      #Creates a dictionary object of all the jerseys for the template
    return render(request, 'JimiJams/JimiJams_index.html', context)

def add_guitar(request):
    form = GuitarForm(request.POST or None)     #Gets the posted form, if one exists
    if form.is_valid():                         #Checks the form for errors, to make sure it's filled in
        form.save()                             #Saves the valid form/jersey to the database
        return redirect('guitar_index')                #Redirects to the index page, which is named 'jimiAdamin'
    else:
        print(form.errors)                      #Prints any errors for the posted form to the terminal
        form = GuitarForm()                     #Creates a new blank form
    return render(request, 'JimiJams/guitar_create.html', {'form':form})

def select_guitar(request, pk):
    pk = int(pk)  # Casts value of pk to an int so it's in the proper form
    guitar = get_object_or_404(Guitar, pk=pk)  # Gets single instance of the guitar from the database
    context = {'guitar': guitar}  # Creates dictionary object to pass the jersey object
    return render(request,'JimiJams/guitar_details.html', context)

def edit_guitar(request, pk):
    guitar = get_object_or_404(Guitar, pk=pk) # get guitar object
    if request.method == "POST":
        form = GuitarForm(request.POST, instance=guitar)  # gets the posted form
        if form.is_valid():  # Checks the form for errors
            guitar = form.save()  # Saves the guitar form
            guitar.save()    # saves the guitar object
            return redirect('guitar_details', pk=guitar.pk)
    else:
        form = GuitarForm(instance=guitar)
    return render(request, 'JimiJams/guitar_edit.html', {'form': form})

def delete_guitar(request, pk):
    guitar = get_object_or_404(Guitar, pk=pk)
    if request.method == "POST":
        guitar.delete()
        return redirect('guitar_index')
    return render(request, "JimiJams/guitar_delete.html", context={'guitar': guitar})

#View function for the main API page with dropdowns
def api_guitar(request):


    return render(request, 'JimiJams/guitar_api.html', context)


######## URLS #########

from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.jimiAdmin, name='jimiAdmin'),  #home page for Jimi Jams App
    path('SeeGuitarCollection/', views.guitarList, name='guitar_index'),
    path('AddGuitar/', views.add_guitar, name='guitar_create'),
    path('SeeGuitarCollection/<int:pk>/Details', views.select_guitar, name='guitar_details'),
    path('SeeGuitarCollection/<int:pk>/Edit/', views.edit_guitar, name='guitar_edit'),
    path('SeeGuitarCollection/<int:pk>/Delete/', views.delete_guitar, name='guitar_delete'),
    path('BuyGuitar/', views.api_guitar, name='guitarApi'),
    ]

#########  Models #########

from django.db import models

# Create your models here.

GUITAR_TYPES = (('Electric', 'Electric'), ('Acoustic', 'Acoustic'), ('Double-Neck', 'Double-Neck'), ('Bass', 'Bass'), ('Seven-String','Seven-String'),
                ('Other', 'Other'))

GUITAR_PICKUP =(('Single-coil', 'Single-coil'), ('Humbucker', 'Humbucker'), ('P90', 'P90'), ('Hybrid', 'Hybrid'), ('Other', 'Other'))


class Guitar(models.Model):
    guitar_name = models.CharField(max_length=30)
    guitar_manufacturer = models.CharField(max_length=30)
    guitar_type = models.CharField(max_length=30, choices=GUITAR_TYPES)
    guitar_color = models.CharField(max_length=30)
    guitar_pickups = models.CharField(max_length=30, choices=GUITAR_PICKUP)
    guitar_cost = models.CharField(max_length=30)
    guitar_wood = models.CharField(max_length=30)

    Guitars = models.Manager()

    def __str__(self):
        return self.guitar_name

################# FORMS ##############

from django.forms import ModelForm
from .models import Guitar

#Create the form class.
class GuitarForm(ModelForm):
    class Meta:
        model = Guitar
        fields = '__all__'

################ Template For Index for Models  ###########################3

{% extends 'JimiJams/JimiJams_base.html' %}
{% load staticfiles %}
{% block templatecontent %}

<section >
    <div class="flex-container footy" id="jerseyCollectionPage">
        <table class="guitar-form">
            <tr>
                <th class="col-md">Guitar Model Name</th>
                <th class="col-md">Brand</th>
                <th class="col-md">Guitar Type</th>
                <th class="col-md">Color</th>
                <th class="col-md">Pickups</th>
                <th class="col-md">Cost</th>
                <th class="col-md">Wood</th>
                <th class="col-md">&nbsp;Info</th>
            </tr>
            {% for Guitar in guitars %}     <!-- creates a new row for each guitar in the collection -->
                <tr>
                    <td class="col-md">{{Guitar.guitar_name}}</td>
                    <td class="col-md">{{Guitar.guitar_manufacturer}}</td>
                    <td class="col-md">{{Guitar.guitar_type}}</td>
                    <td class="col-md">{{Guitar.guitar_color}}</td>
                    <td class="col-md">{{Guitar.guitar_pickups}}</td>
                    <td class="col-md">{{Guitar.guitar_cost}}</td>
                    <td class="col-md">{{Guitar.guitar_wood}}</td>
                    <td class="col-md"><a href="{{Guitar.pk}}/Details"><button class="collection-btn-jimi1" id="info-button">Details</button></a></td>
                </tr>
            {% endfor %}
        </table>
        <button class="collection-btn-jimi1" type="button" onclick=" location.href='{% url 'guitar_create' %}'">Add to Collection</button>
    </div>
</section>
{% endblock %}

########################### Template for Home ######################################


{% extends 'JimiJams/JimiJams_base.html' %}
{% load staticfiles %}
{% block templatecontent %}
<section id="jimiwelcome">

    <strong>Welcome to the Jimi Jams Page!</strong> <br /><br ?>
    This site is dedicated to help guitarists collect, find, and buy guitars!<br />
    Here you can manage your guitar collection, find guitars similiar to what Jimi Hendrix played, and buy new guitars!<br />

</section>

{% endblock %}

###################################### Template for Base ########################################

{% extends 'base.html' %}
{% load staticfiles %}

{% block pagetop-css %}cover-jimi{% endblock%}

{% block page-title%}<div class="jimi-title">Jimi Jams</div>{% endblock %}
{% block page-subtitle %} <div class="jimi-header">Find the gear of the greats today!</div>{% endblock %}
{% block button1 %}<a href="{% url 'guitar_index'%}" class="contact-btn-jimi"> See Collection </a>{% endblock %}
{% block button2 %}<a href= "" class="contact-btn-jimi"> Find Guitars </a>{% endblock %}
{% block button3 %}<a href="{% url 'guitarApi' %}" class="contact-btn-jimi"> Buy Guitars </a>{% endblock %}
{% block appcontent %}

<section>

    {% block templatecontent %}{% endblock%}
{% endblock %}

###########################################3 Template for Details #######################################

{% extends 'JimiJams/JimiJams_base.html' %}
{% load staticfiles %}
{% block templatecontent %}

<section>
    <div class="flex-container footy">
        <table>
            <tr>
                <th>Guitar Model Name:</th>
                <td>{{guitar.guitar_name}}</td>
            </tr>
            <tr>
                <th>Brand:</th>
                <td>{{guitar.guitar_manufacturer}}</td>
            </tr>
            <tr>
                <th>Guitar Type:</th>
                <td>{{guitar.guitar_type}}</td>
            </tr>
            <tr>
                <th>Color:</th>
                <td>{{guitar.guitar_color}}</td>
            </tr>
            <tr>
                <th>Pickups:</th>
                <td>{{guitar.guitar_pickups}}</td>
            </tr>
            <tr>
                <th>Cost:</th>
                <td>{{guitar.guitar_cost}}</td>
            </tr>
            <tr>
                <th>Wood:</th>
                <td>{{guitar.guitar_wood}}</td>
            </tr>
        </table>

        <hr />
        <br />
        <button class="collection-btn-jimi1" type="button" onclick=" location.href='{% url 'guitar_edit' guitar.pk %}'"> Update Guitar Details
        </button>
        <br />
        <button class="collection-btn-jimi1" type="button" onclick=" location.href='{% url 'guitar_delete' guitar.pk %}'">Delete Guitar
        </button>
        <br />
        <button class="collection-btn-jimi1" type="button" onclick=" location.href='{% url 'guitar_index' %}'">Back to Collection</button>
        <br />
        <br />
    </div>
</section>
{% endblock %}



############################# Template for Create #####################################################################3


{% extends 'JimiJams/JimiJams_base.html' %}
{% load staticfiles %}
{% block templatecontent %}

<section>
    <div class="flex-container">
        <form method="post">
            {% csrf_token %}
            <table class="guitar-form">
                {{ form.as_table }}
            </table>
            {{ form.non_field_errors }}
            <br />
            <button class="collection-btn-jimi1" type="submit"> Add to Collection </button>
            <button class="collection-btn-jimi2" type="button" onclick=" location.href='{% url 'guitar_index' %}'">Back to Collection</button>
        </form>
        <br />
        <br />
    </div>
</section>
{% endblock %}






############################################# Tempalte for Delete ################################################3

{% extends 'JimiJams/JimiJams_base.html' %}
{% load staticfiles %}
{% block templatecontent %}
    <div class="flex-container footy">

        <form method="post">

            {% csrf_token %}
            <br />
            <br />
            <h1 class = "guitar-delete">Are you sure you want to delete {{guitar.guitar_name}}?</h1>
            <br />
            <br />
            <button class="collection-btn-jimi1" type="submit">Delete Guitar</button>
            <br />
            <button class="collection-btn-jimi1" type="button" onclick="location.href='{% url 'guitar_index' %}'"> Return to collection </button>
            <br />

        </form>
    </div>
{% endblock %}


############################################ Template for Edit #######################################3

{% extends 'JimiJams/JimiJams_base.html' %}
{% load staticfiles %}
{% block templatecontent %}
<section>
    <div class="flex-container footy">
        <form method="post">
            {% csrf_token %}
            <table>
                {{ form.as_table }} <!-- this only renders the td tags, still need the table tags -->
            </table>
            {{ form.non_field_errors }}
            <button class="collection-btn-jimi1" type="submit">Save</button>
        </form>
        <br />
        <button class="collection-btn-jimi1" type="button" onclick="location.href='{% url 'guitar_index' %}'"> Return to Guitar Collection </button>
        <br />
    </div>
</section>
{% endblock %}


################################# CSS Styling ############################################3



/* ===============Jimi Jams Style====================== */
.cover-jimi {
    background: url('../images/jimihome.jpg') center;
    filter: sepia(45%);
    opacity: 0.9;
    background-size: cover;
    background-repeat: no-repeat;
    height: 65vh;
  }

#jimiwelcome {
    font-size: 1.5vw;
    display:inline-block;
    padding:2px 3px;
    width: 100%;
    margin-top: 50px;
    margin-bottom: 50px;
    text-align: center;
    line-height:1.5em;
}

.contact-btn-jimi {
    display: inline-block;
    margin-right: 2vw;
    margin-left: 2vw;
    margin-bottom: 5vw;
    padding: 15px 30px;
    border: 1px solid white;
    border-radius: 7px;
    background: black;
    opacity: 0.75;
    color: white ;
    text-decoration: none;
    transition: 0.3s;
    font-weight: bold;
    font-size: 1.75vw;
}

.contact-btn-jimi:hover {
  background: white;
  color: black;
}

.jimi-title {
 color: black;
 font-weight: bold;
 font-size: 4.5vw;
 margin-top: 1.5vw;
}

.jimi-header {
 color: black;
 font-weight: bold;
 font-size: 2.5vw;
 margin-top: 1.5vw;
 }

.collection-btn-jimi1 {
    display: inline;
    margin-right: 2vw;
    margin-left: 32vw;
    padding: 10px 20px;
    border: 1px solid white;
    border-radius: 7px;
    background: black;
    opacity: 0.75;
    color: white ;
    text-decoration: none;
    transition: 0.3s;
    font-weight: bold;
    font-size: 1vw;
}

.collection-btn-jimi2 {
    display: inline;
    margin-right: 2vw;
    margin-left: 2vw;
    padding: 10px 20px;
    border: 1px solid white;
    border-radius: 7px;
    background: black;
    opacity: 0.75;
    color: white ;
    text-decoration: none;
    transition: 0.3s;
    font-weight: bold;
    font-size: 1vw;
}


.collection-btn-jimi1:hover {
  border: 1px solid black;
  background: white;
  color: black;
}

.collection-btn-jimi2:hover {
  border: 1px solid black;
  background: white;
  color: black;
}


.guitar-form{
    background: black;
    opacity: 0.75;
    margin-top: 3vw;
    margin-bottom: 1.5vw;
    margin-left: 30vw;
    font-size:1.33vw;
}

#id_guitar_name{
    font-size:1.33vw;
    width: 16vw;
}

#id_guitar_manufacturer{
    font-size:1.33vw;
    width: 16vw;
}

#id_guitar_type{
    font-size:1.33vw;
    width: 16vw;
   }

#id_guitar_color{
    font-size:1.33vw;
    width: 16vw;
}

#id_guitar_pickups{
    font-size:1.33vw;
    width: 16vw;
}

#id_guitar_cost{
    font-size:1.33vw;
    width: 16vw;
}

#id_guitar_wood{
    font-size:1.33vw;
    width: 16vw;
}

.guitar-delete{
    margin-left: 35vw;
    font-size: 1.33vw;
}