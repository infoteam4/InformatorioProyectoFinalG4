from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .models import *
from .forms import *
import datetime
import time
from .filters import turnoFilter, turnoFilteradmin

from django.utils.dateparse import parse_date

# Create your views here.

def home(request):

    novedad1 = Novedad.objects.get(id = 1)
    context = {'novedad1' : novedad1}
    return render(request, 'home.html', context)

def registro(request):
    if request.user.is_authenticated:
        return redirect('paciente')
    else:
        form = RegistrarPacienteForm()
        if request.method == 'POST':
            form = RegistrarPacienteForm(request.POST)
            nombre_f = request.POST.get('nombre')
            apellido_f = request.POST.get('apellido')
            dni_f = request.POST.get('dni')
            tel_f = request.POST.get('tel')
            fecha_f = request.POST.get('fecha')
            os_f = request.POST.get('os')
            email_f = request.POST.get('email')

            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                idusuario= User.objects.get(username = username)
                
                Paciente.objects.create(            
                    user = idusuario,
                    dni = dni_f, 
                    nombre = nombre_f,
                    apellido = apellido_f,
                    email = email_f,
                    tel = tel_f,
                    fecha = fecha_f,
                    os = os_f
                    ) 
                messages.success(request, 'El usuario ' + username + ' fue creado exitosamente')
                return redirect('login')

        context = {'form':form}
        return render(request, 'registro.html', context)

def loginPaciente(request):
    if request.user.is_authenticated:
        return redirect('paciente')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('paciente')
            else:
                messages.info(request, 'Usuario y/o contraseñas incorrectas',user)

        
        return render(request, 'login.html', )

def logoutPaciente(request):
  logout(request)
  return redirect('login')


@login_required(login_url = 'login')
def elegirServicio(request):
    if request.method == 'POST':
        servicio = request.POST.get("servicio")
        if servicio != 'Elegir servicio':
            idservicio = Servicio.objects.get(nombre=servicio).id
            return redirect('sacarTurno',idservicio)
        else:
            messages.info(request, 'Elija un servicio para continuar')
            
        
    
    servicios = Servicio.objects.all()
    context = {'servicios':servicios}

    return render(request, 'elegirservicio.html', context)


@login_required(login_url = 'login')
def sacarTurno(request,pk):
    
    servicio = Servicio.objects.get(id=pk)
    paciente = Paciente.objects.get(user_id=request.user.id) #tiene que estar loggeado si o si y ahi obtengo el user id
    practicas = Practica.objects.filter(servicio=servicio.id)
    turnos = Turno.objects.filter(estado = 'Libre', servicio = servicio.id,) #paciente = "paciente"
    context = {'paciente':paciente,'servicio':servicio,'paciente':paciente,'practicas':practicas, 'turnos': turnos}
    
    if request.method == 'POST':
        
        practica_select = request.POST.get("practica")
        practica = Practica.objects.get(nombre = practica_select)
        turno_select = request.POST.get("turno")[22]
        turnod = int(turno_select)
        #print(turnod)
        #turno = Turno.objects.get(nombre = turno_select)
        #esta parte hay que pulir necesitamos obtener el id de la practica para hacer el  update en la tabla turno
      
        #turno_id = Turno.objects.get(estado = 'Libre',)
        time_str = request.POST.get('turno')[11:19]
        date_str = request.POST.get('turno')[0:10]
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        
        #print(time_str) 
        time =  datetime.datetime.strptime(time_str, "%H:%M:%S").time()
        print(time)       
        # print(time_str)  
        #print(date)      
        
        reserva = Turno.objects.get(id = turnod) #fecha = date
        reserva.paciente = paciente
        reserva.estado = 'Reservado'
        reserva.practica = practica
        reserva.save()
       
        return redirect('turnoConfirmado',reserva.id)
    
    return render(request, 'formturnos.html', context)


@login_required(login_url = 'login')
def cancelarReserva(request):
    context = {}
    return render(request, 'eliminacion.html', context)


@login_required(login_url = 'login')
def paciente(request):
    paciente = Paciente.objects.get(user_id = request.user.id)
    
    turnos = Turno.objects.filter(paciente = paciente.id)
    miFiltro = turnoFilter(request.GET, queryset = turnos)
    turnos = miFiltro.qs

    turnosadmin = Turno.objects.all()
    miFiltroadmin = turnoFilteradmin(request.GET, queryset = turnosadmin)
    turnosadmin = miFiltroadmin.qs

    novedad1 = Novedad.objects.get(id = 1)

    context = {'paciente':paciente, 'turnos':turnos, 'miFiltro':miFiltro, 'miFiltroadmin':miFiltroadmin, 'novedad1':novedad1, 'turnosadmin': turnosadmin}
    return render(request, 'paciente.html', context)


@login_required(login_url = 'login')
def misDatos(request):
    
    paciente = Paciente.objects.get(user_id = request.user.id)
    if request.method == 'POST':
        
        paciente.nombre = request.POST.get('nombre')
        paciente.apellido = request.POST.get('apellido')
        paciente.dni = request.POST.get('dni')
        paciente.tel = request.POST.get('tel')
        paciente.fecha = request.POST.get('fecha')
        paciente.os = request.POST.get('os')
        paciente.email = request.POST.get('email')

        paciente.save()

        messages.success(request, 'Se modificaron sus datos exitosamente')
        return redirect('paciente')


    context = {'paciente':paciente}
    return render(request, 'misdatos.html', context)    


@login_required(login_url = 'login')
def turnoConfirmado(request,pk):
    turno = Turno.objects.get(id = pk)

    context = {'turno':turno}
    return render(request, 'turnoconfirmado.html', context)


@login_required(login_url = 'login')
def modifServicio(request,pk):
    
    if request.method == 'POST':
        servicio = request.POST.get("servicio")
        idservicio = Servicio.objects.get(nombre=servicio).id
        request.session['turno'] = turno_reservado = Turno.objects.get(id = pk).id
        return redirect('modifTurno',idservicio)
        """ servicios = Servicio.objects.all()
        context = {'servicios':servicios} """
    else:
        turno_reservado = Turno.objects.get(id = pk).servicio
        serv_reservado = Servicio.objects.get(nombre = turno_reservado)
        servicios = Servicio.objects.all()

        context = {'servicios':servicios,'serv_reservado':serv_reservado}   

    return render(request, 'modifServicio.html', context)


@login_required(login_url = 'login')
def modifTurno(request,pk):
    turno_reservado = request.session['turno']
    servicio = Servicio.objects.get(id=pk)
    paciente = Paciente.objects.get(user_id=request.user.id) #tiene que estar loggeado si o si y ahi obtengo el user id
    practicas = Practica.objects.filter(servicio=servicio.id)
    turnos = Turno.objects.filter(estado = 'Libre', servicio = servicio.id,) #paciente = "paciente"
    context = {'paciente':paciente,'servicio':servicio,'paciente':paciente,'practicas':practicas, 'turnos': turnos,'turno_reservado':turno_reservado}
    
    if request.method == 'POST':
        
        practica_select = request.POST.get("practica")
        practica = Practica.objects.get(nombre = practica_select)
        turno_select = request.POST.get("turno")[22]
        turnod = int(turno_select)
        #print(turnod)
        #turno = Turno.objects.get(nombre = turno_select)
        #esta parte hay que pulir necesitamos obtener el id de la practica para hacer el  update en la tabla turno
      
        #turno_id = Turno.objects.get(estado = 'Libre',)
        time_str = request.POST.get('turno')[11:19]
        date_str = request.POST.get('turno')[0:10]
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        
        #print(time_str) 
        time =  datetime.datetime.strptime(time_str, "%H:%M:%S").time()
        print(time)       
        # print(time_str)  
        #print(date)     
        liberado = Turno.objects.get(id = turno_reservado) #fecha = date
        liberado.paciente = None
        liberado.estado = 'Libre'
        liberado.practica = None
        liberado.save() 
        
        editado = Turno.objects.get(id = turnod) #fecha = date
        editado.paciente = paciente
        editado.estado = 'Reservado'
        editado.practica = practica
        editado.save()
       
        return redirect('turnoModificado',editado.id)
    
    return render(request, 'modifturno.html', context)


@login_required(login_url = 'login')
def turnoModificado(request,pk):
    turno = Turno.objects.get(id = pk)

    context = {'turno':turno}
    return render(request, 'turnoModificado.html', context)


@login_required(login_url = 'login')
def cancelarTurno(request,pk):
    turno = Turno.objects.get(id = pk)
    if request.method == 'POST':
        turno.paciente = None
        turno.estado = 'Libre'
        turno.practica = None
        turno.save() 
        return redirect('paciente')
    context = {'turno':turno}
    return render(request, 'eliminacion.html', context)

def altaServicio(request):
    if request.method == 'POST':
        nombre_s = request.POST.get('servicio')
        Servicio.objects.create(            
                nombre = nombre_s,
                )
        messages.success(request, 'Servicio ' + nombre_s + ' agregado exitosamente!')
        return redirect('altaServicio')

    return render(request, 'crearservicio.html')

def altaPractica(request):
    servicios = Servicio.objects.all()
    context = {'servicios': servicios}
    if request.method == 'POST':
        nombre_p = request.POST.get('practica')
        descripcion_p = request.POST.get('descripcion')
        serv_nombre = request.POST.get('servicio')
        servicio_id = Servicio.objects.get(nombre = serv_nombre)

        Practica.objects.create(            
                nombre = nombre_p,
                descripcion = descripcion_p,
                servicio = servicio_id,
                )
        messages.success(request, 'Practica ' + nombre_p + ' agregado exitosamente!')
        return redirect('altaPractica')

    return render(request, 'crearpractica.html', context)

def modifNovedades(request):

    novedad1 = Novedad.objects.get(id = 1)
    context = {'novedad1':novedad1}
    if request.method == 'POST':
        textonovedades = request.POST.get('textonovedades')
        novedad1.descripcion = textonovedades
        novedad1.save()
        
        return redirect('paciente')

    return render(request, 'modificarnovedades.html', context)