# Proyecto de votaciones 
###### Kevin Andres Usama Trespalacios


### Acerca de este proyecto 
Este proyecto es el resultado de una prueba técnica de un sistema de información de votaciones con Python, Django Rest Framework y MySQL

### Requerimientos del proyecto
Los Requerimientos de este proyecto son los siguientes:

- Este sistema debe ser una API Rest usando JSON como método de transporte de los datos.
- Tener un servicio de Login (usuario y contraseña), que permita obtener un Token para consumir el resto de servicios.
- El sistema deberá validar la existencia del Token en los servicios, para permitir acceder a la información.
- Cada servicio creado, debe tener un CRUD básico para gestionar la información.
- Exponer servicios que permitan realizar la gestión de Departamentos, Municipios, y mesas de votación.
- Exponer un servicio que permita obtener la cantidad total de votantes inscritos por líder.
- Exponer un servicio que permita obtener la cantidad total de votantes, en el sistema.
- Exponer un servicio que permita obtener la cantidad total de votantes inscritos por municipio.
- Exponer un servicio que permita obtener la cantidad total de votantes inscritos por mesa de votación.

### Estructura del Proyecto
Este proyecto se basa en la estructura de un proyecto predeterminado de Django, con la libreria Rest Framework, contiene un archivo models.py donde se guardan las clases modelo que serán las tablas de la base de datos, un archivo general_serializers.py, donde se encuentran todos los serializers que se encargarán de transformar la información de los modelos a Json, una carpeta views donde contiene las vistas del proyecto, ahi se resguardarán los archivos que le darán las funcionalidades y la logica al sistema, gracias a los serializers.

#### Modelos del archivo Models.py:
- **UserManager:** Se encargá de gestionar la creación de los usuarios en el sistema, ya sea un usuario que no es staff, o un usuario "superuser", en este caso el usuario que no es staff es un "Lider", y el usuario "superuser" sería un Administrador del sistema.
- **Lider:** Este modelo es el rol Lider de nuestro sistema.
- ** User:** Este modelo se encarga de extender la información del modelo lider, agregandole un documento por el cual estas dos clases se relacionan, ya que es necesario tener el modelo User para la autenticación de los usuarios en el sistema, por eso se extiende de Lider.
- **Votantes:** Este modelo se encarga de crear la tabla para los votantes, que serán las personas que el usuario Lider registre en el sistema, esta tabla esta relacionada con el id del lider que lo registre, el municipio donde tendrá que votar, y el puesto de votación donde tendrá que asistir.
- **PuestoVotacion:** Este modelo se encarga de crear la tabla para los puestos de votación.
- **Municipios:** Este modelo se encarga de crear la tabla para los municipios que se vayan a crear, esta relacionada con un departamento de la tabla Departamentos.
- ** Departamentos:** Este modelo se encarga de crear la tabla para los departamentos que tendrá el sistema.

#### Archivos de la carpeta Views:
##### usuarios_views.py:
Este archivo .py, se conforma por una clase llamada UsuariosViewSet, que se encarga de crear los metodos de gestión de los Usuarios, gracias al UsuarioSerializer, esta clase tiene los metodos **get_queryset, create, update, partial_update y destroy**.
Tambien incluye un metodo llamado LiderViewSet, que se encarga de crear los metodos de gestión de los Lideres, gracias al LiderSerializer, en esta clase se gestiona tanto los Lideres, como los Usuarios, ya que en el sistema, cuando creas un Lider, tambien creas un usuario a la vez, ya que necesitamos el usuario para la autenticacion, esta clase tambien tiene los metodos **get_queryset, create, update y destroy**, y cuenta con la **validacion** de que **no se pueda crear otro lider con el mismo numero de documento.**
Ademas al final del archivo se encuentra una** validación** que se hace cada **60 segundos,** donde mira si se han creado nuevos votantes con el id de cada Lider, si hay un nuevo votante que registró un lider, **este numero se actualiza en el campo cantidad_votantes** de los lideres, para asi ver cuantos votantes han registrado cada lider, **este campo y validación tambien se encuentra en otros archivos como el de municipios_departamentos_views.py y puesto_votacion_views.py, para lograr determinar cuantos votantes tiene cada municipio creado y cada puesto de votacion creado.**

##### municipios_departamentos_views.py:
Este archivo contiene las clases MunicipiosViewSet y DepartamentosViewSet, ambas clases contienen los metodos **get_queryset, create, update y destroy** para asi poder gestionar la información gracias a sus serializers.

##### puesto_votacion_views.py:
Este archivo contiene la clase PuestoVotacionViewSet, que contiene los metodos **get_queryset, create, update y destroy** para poder gestionar la información de estos puestos gracias a su serializer.

##### votantes_views.py:
Este archivo contiene la clase VotantesViewSet, que contiene los metodos **get_queryset, create, update y destroy** para poder gestionar la información de los votantes gracias a su serializer, esta clase tambien tiene la validación para que no se puedan registrar votantes con el mismo numero de documento.

##### auth_token_views.py:
Este archivo contiene las clases **UserToken, Login y Logout**, estas clases se encargan de la gestión de la autenticación en el sistema, que junto a validaciones logra un metodo de autenticación con la ayuda de un Token por usuario, ademas, la autenticacion se refuerza con una clase llamada **authentication.py** que se encuentra en la carpeta **authentication** en la app del proyecto **"GlobalApi"**, la clase **Login** permite **ingresar credenciales "username" que en este caso es el documento de los lideres o del Administrador, y la credencial "password", que es la contraseña de los usuarios**, si las credenciales son correctas devuelve un **Token**, que se puede usar para consumir el resto del sistema y sus funcionalidades.
La clase **Logout permite borrar un Token de un usuario** ingresando dicho token.
La clase **UserToken**, permite consultar y refrescar el token de un usuario ingresando su numero de documento.
El sistema tambien cuenta con una **expiración de un token cada 1 hora**, por lo tanto, se tendría que refrescar este token con la clase **UserToken**, no es necesario iniciar sesión otra vez, ya que el token se crea **automaticamente**.

### Permisos de usuarios
El rol **Administrador** que es un super usuario, podrá gestionar y ver toda la información del sistema.
El rol **Lider** solo puede gestionar la información de los votantes que ellos registren, si consultan votantes, el sistema solo muestra sus votantes, si los crea el sistema les agrega automaticamente el id del lider que los agregó, si los actualiza, no se le puede actualizar el id del lider, y no podrá actualizar votantes que tengan id de otros lideres, y solo podrá borrar los votantes que tengan el id del lider que los registró.

### Endpoints del API:
**LOGIN: **
http://127.0.0.1:8000/ POST
Se ingresa en el **Body** en tipo **form-data **dos campos, el primer campo es el "username", que en el key va el documento del usuario que iniciará sesión y el segundo campo es el "password", que se ingresará la contraseña del usuario.

**LOGOUT:**
http://127.0.0.1:8000/logout/?token= **GET**
Se ingresa en **Params** el Key "token" y en Value se ingresa el token del usuario que cerrará sesión, borrando asi su token.

**Consultar y refrescar token del usuario:**
http://127.0.0.1:8000/refresh-token?username= **GET**
Se ingresa en **Params** en el campo key "username" y en el valor se ingresa el numero de documento del usuario que se quiere consultar el token.

**Ver y consultar Lideres:** 
http://127.0.0.1:8000/modulos/lideres/ **GET**
Se ingresa en **Headers** en el campo Key "Authorization", y en el campo Value se ingresa "Token (Token del usuario)", solo el admin puede ver los Lideres.

**Registrar lideres:**
http://127.0.0.1:8000/modulos/lideres/ **POST**
En **Headers** se ingresa "Authorization" en el campo Key, y se ingresa "Token (Token del usuario)" en el campo Value, despues en Body se ingresa el siguiente esqueleto en formato Json para la creación del Lider, se rellena la información, en doc_lider es donde se crea el usuario a la vez que el lider, y se agrega un doc que será el identificador de este lider, el username, y el password que será la contraseña para la autenticación.

```json
{
    "nombres_lider": "",
    "apellidos_lider": "",
    "direccion_lider": "",
    "ciudad_lider": "",
    "foto_lider": null,
    "email_lider": "",
    "doc_lider": {
           "doc": "",
           "username": "",
           "password": ""
    }
}
```
**Actualizar Lideres:** 
http://127.0.0.1:8000/modulos/lideres/( id del lider para actualizar )/ **PUT**
En **Headers** se pone el Authorization y el Token en Value, despues en Body para actualizar se pega el esqueleto del lider al que quiere actualizar (No se podrá actualizar el id del lider, ni la información del user como el doc o la contraseña, ni tampoco el campo cantidad_votantes).  Tambien se puede pegar el Json del Lider que se obtiene de la **Consulta de Lideres**.
```json
    {
        "id_lider": ,
        "nombres_lider": "",
        "apellidos_lider": "",
        "direccion_lider": "",
        "ciudad_lider": "",
        "foto_lider": null,
        "email_lider": "@gmail.com",
        "cantidad_votantes": 0,
        "doc_lider": ""
    }
```
**Borrar Lider**:
http://127.0.0.1:8000/modulos/lideres/( id del lider que se quiere borrar )/ **DELETE**
Se ingresan los datos de autenticación en **Headers**, despues se envia la solicitud de eliminación.

**Ver cantidad de votantes creados:**
http://127.0.0.1:8000/modulos/total_votantes/ **GET**
Se ingresa los datos de autenticación en **Headers**, despues se envia la solicitud de GET y obtendrá una respuesta con un mensaje mostrando cuantos votantes en total hay en el sistema.

**Para obtener el resto de endpoints es necesario la colección Postman, se ingresan los mismos datos de autenticación en los endpoints.**

**Esqueletos para crear resto de objetos:**

**Municipio:** 
```json
{
    "nombre_municipio": "",
    "departamento_municipio": (ID DEL DEPARTAMENTO QUE SE QUIERE AGREGAR)
}
```
**Puesto de votacion:**
```json
{
    "nombre_puesto_votacion": "",
    "direccion_puesto_votacion": "",
    "municipio_puesto_votacion": (ID DEL MUNICIPIO QUE SE QUIERE AGREGAR)
}
```
**Votante:**
```json
{
    "doc_votante": "",
    "nombres_votante": "",
    "apellidos_votante": "",
    "direccion_votante": "",
    "municipio_votante": (ID DEL MUNICIPIO),
    "puesto_votacion": (ID DEL PUESTO DE VOTACION),
    "lider_id": (ID DEL LIDER)
}
```
**Departamento:**

```json
{
    "nombre_departamento": ""
}
```

**Para la actualización de estos objetos se puede tomar el esqueleto de donde se consultan o listan cada objeto, se copia y pega el objeto que se quiere actualizar y se le modifican los datos.**



**Muchas gracias por leer mi codigo, espero que se haya podido entender lo mas que pueda este archivo README.**

**FIN**

