# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required
from django.db import connections

##Orden de importacion es orden en que se realiza ETL
from django.contrib.auth.models import User, Group
from apps_cenco.db_app.models import Sucursal, Encargado, Alumno, Empleado, Carrera, Telefono, Expediente
from apps_cenco.db_app.models import Colegiatura, DetallePago, Horario, Grupo, Inscripcion, Asistencia
from apps_cenco.db_app.models import Estado, DetalleEstado, Materia, DetallePensum, Cursa, Examen, Evaluacion

# Create your views here.

def principal(request):
    if request.user.is_authenticated:
        if has_group(request.user, 'Director'):
            return redirect('ingreso_retiros_estudiantes')

        elif has_group(request.user, 'Profesor'):
            return redirect('desempenio_estudiantil')

        elif has_group(request.user, 'Supervisor'):
            return redirect('ingreso_econ_suc')
        elif request.user.is_superuser:
            return redirect('etl')
    else:
        return redirect('login')


def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


def verPantallaETL(request):
    msj = ""
    esDanger = False
    if request.method == 'POST':
        try:
            ##LIMPIANDO LA BD GERENCIAL
            User.objects.filter(is_superuser = False).delete() ##Eliminacion en Cascada, alv
            #Group.objects.all().delete()
            # with connections['default'].cursor() as cursorST:
            #     cursorST.execute("DELETE FROM AUTH_USER_GROUPS")
            # DetallePago.objects.all().delete()
            # Colegiatura.objects.all().delete()
            # Expediente.objects.all().delete()
            # Telefono.objects.all().delete()
            # Encargado.objects.all().delete()
            # Alumno.objects.all().delete()
            # Empleado.objects.all().delete()
            # Carrera.objects.all().delete()
            # Sucursal.objects.all().delete()

            ## EXTRAYENDO Y GUARDANDO DE ST A SG
            usuarios = User.objects.using('st_cenco').filter(is_superuser= False)
            grupos = Group.objects.using('st_cenco').all()
            for usuarioST in usuarios:
                usuarioST.save(using='default') ##Save guarda usando BD Default
            for grupoST in grupos:
                grupoST.save(using='default')
            with connections['st_cenco'].cursor() as cursorST:
                cursorST.execute("SELECT * FROM AUTH_USER_GROUPS")
                filas = cursorST.fetchall()
            with connections['default'].cursor() as cursorSG:
                for fila in filas:
                    cursorSG.execute("INSERT INTO AUTH_USER_GROUPS VALUES({}, {}, {})".format(fila[0], fila[1], fila[2]))
                cursorSG.execute("SELECT * FROM AUTH_USER_GROUPS")
            sucursales = Sucursal.objects.using('st_cenco').all()
            for sucursalST in sucursales:
                sucursalST.save(using='default')
            encargados = Encargado.objects.using('st_cenco').all()
            for encargadoST in encargados:
                encargadoST.save(using='default')
            alumnos = Alumno.objects.using('st_cenco').all()
            for alumnoST in alumnos:
                alumnoST.save(using='default')
            empleados = Empleado.objects.using('st_cenco').all()
            for empleadoST in empleados:
                empleadoST.save(using='default')
            carreras = Carrera.objects.using('st_cenco').all()
            for carreraST in carreras:
                carreraST.save(using='default')
            telefonos = Telefono.objects.using('st_cenco').all()
            for telefonoST in telefonos:
                telefonoST.save(using='default')
            expedientes = Expediente.objects.using('st_cenco').all()
            for expedienteST in expedientes:
                expedienteST.save(using='default')
            colegiaturas = Colegiatura.objects.using('st_cenco').all()
            for colegiaturaST in colegiaturas:
                colegiaturaST.save(using='default')
            detallesPagos = DetallePago.objects.using('st_cenco').all()
            for detallePagoST in detallesPagos:
                detallePagoST.save(using='default')
            horarios = Horario.objects.using('st_cenco').all()
            for horarioST in horarios:
                horarioST.save(using='default')
            gruposClases = Grupo.objects.using('st_cenco').all()
            for grupoClaseST in gruposClases:
                grupoClaseST.save(using='default')
            inscripciones = Inscripcion.objects.using('st_cenco').all()
            for inscripcionST in inscripciones:
                inscripcionST.save(using='default')
            asistencias = Asistencia.objects.using('st_cenco').all()
            for asistenciaST in asistencias:
                asistenciaST.save(using='default')
            estados = Estado.objects.using('st_cenco').all()
            for estadoST in estados:
                estadoST.save(using='default')
            detalleEstados = DetalleEstado.objects.using('st_cenco').all()
            for detalleEstadoST in detalleEstados:
                detalleEstadoST.save(using='default')
            materias = Materia.objects.using('st_cenco').all()
            for materiaST in materias:
                materiaST.save(using='default')
            detallePensums = DetallePensum.objects.using('st_cenco').all()
            for detallePensumST in detallePensums:
                detallePensumST.save(using='default')
            cursas = Cursa.objects.using('st_cenco').all()
            for cursaST in cursas:
                cursaST.save(using='default')
            examenes = Examen.objects.using('st_cenco').all()
            for examenST in examenes:
                examenST.save(using='default')
            evaluaciones = Evaluacion.objects.using('st_cenco').all()
            for evaluacionST in evaluaciones:
                evaluacionST.save(using='default')



            ### Corrigiendo sequence de auth_user, los demas no se espera insecion de usuarios
            with connections['default'].cursor() as cursorSG2:
                cursorSG2.execute('Select max(id) from auth_user;')
                id_max = cursorSG2.fetchone()
                print 'max id:' + str(id_max);
                cursorSG2.execute("alter sequence auth_user_id_seq restart with {}".format(str(id_max[0] + 1)))
                cursorSG2.execute('Select max(id) from auth_user_groups;')
                id_max = cursorSG2.fetchone()
                cursorSG2.execute("alter sequence auth_user_groups_id_seq restart with {}".format(str(id_max[0] + 1)))


            msj = "ETL finalizado con exito"
        except:
            msj = "Ocurrió un Error al realizar el ETL, notificar a Técnico"
            print msj
            esDanger = True
    context = {
        'msj' : msj,
        'esDanger' : esDanger
    }
    return render(request, 'Login/etl.html', context)