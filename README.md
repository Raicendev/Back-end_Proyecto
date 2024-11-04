# Proyecto final. Desarrollo de una Plataforma de Venta de Productos
________________________________________________________________________________________________________
En esta practica, Se van a manejar operaciones CRUD basicas y avanzadas,
asi como integrar una autenticacion OAuth2. Como framework para el desarrollo de la API 
se va a utilizar FastAPI, y la base de datos debera de esta alojada en los servidores de MongoDB Atlas.
________________________________________________________________________________________________________
## Creación de un usuario

Basate en este formato de JSON:

**{"id":"", "username": "root", "password": "12345678", "email": "root@localhost.com", "is_admin": true}**

1. El id, se autogenera, se puede dejar vacio. ✔

2. En password la contraseña que desees usar la debes de encriptar en esta pagina web: https://bcrypt-generator.com/ ✔

3. Una vez encriptada la contraseña, debes de copiarla en el valor "password". ✔

*📝No tienes que guardar la contraseña encriptada, cuando se requiera del campo password, puedes poner la contraseña no encriptada*

4. En el campo "is_admin" si quieres tener privilegios para realizar todas las operaciones CRUD debes de poner true ✔

## Creación de un producto:
Basate en este formato de JSON:

**{"id": "", "id_producto": 1 ,"nombre": "camiseta", "descripcion": "azul y verde", "precio": 30.58, "categoria":"ropa", "stock": 10}**

*📝El campo "id_producto" no se puede repetir*

## Creación de un pedido:
Basate en este formato JSON

**{"id":"66522d493825ddee0bacfd10", "cod_order": 1,"username": "juanjo", "id_product": "6650f5a5d0a7edc8607519b1"}**

*📝El campo "cod_order" no se puede repetir*
________________________________________________________________________________________________________

## Los Endpoints que se han implementado son:

- Crear Producto: Endpoint para crear un nuevo producto en la plataforma.
Deberá recibir los datos del producto y almacenarlos en la base de datos. 📤

- Listar Productos: Endpoint para listar todos los productos disponibles en la
plataforma. 📥

- Actualizar Producto: Endpoint para actualizar la información de un producto
existente. Deberá recibir el ID del producto a actualizar y los nuevos datos a
modificar. 📤

- Eliminar Producto: Endpoint para eliminar un producto de la plataforma.
Deberá recibir el ID del producto a eliminar y eliminarlo de la base de datos. 📤

- Buscar Producto por ID: Endpoint para buscar un producto específico por
su ID. 📥

- Buscar Producto por Nombre: Endpoint para buscar productos por su
nombre o una parte del mismo. 📥

- Listar Productos por Categoría: Endpoint para listar productos filtrados por
una categoría específica. 📥

- Listar Productos por Precio: Endpoint para listar productos ordenados por
precio, ya sea de forma descendente. 📥

- Actualizar Stock de Producto: Endpoint para actualizar el stock disponible
de un producto. 📤

- Eliminar Productos por Categoría: Endpoint para eliminar todos los
productos de una categoría específica. 📤

- Buscar usuario por ID:  Endpoint para buscar un usuario específico por
su ID. 📥

- Listar usuario: Endpoint para listar todos los usuarios disponibles en la
plataforma. 📥

- Crear usuario: Endpoint para crear un nuevo usuario en la plataforma.
Deberá recibir los datos del usuario y almacenarlos en la base de datos. 📤

- Actualizar usuario: Endpoint para actualizar la información de un usuario
existente. Deberá recibir el ID del usuario a actualizar y los nuevos datos a
modificar. 📤
  
- Eliminar usuario: Endpoint para eliminar un usuario de la plataforma.
Deberá recibir el ID del usuario a eliminar y eliminarlo de la base de datos. 📤
  
- Creación de registro: Endpoint para crear un registro con autenticacion OAuth2. 📤

- Crear pedido: Endpoint para crear un nuevo producto en la plataforma.
Deberá recibir los datos del producto y almacenarlos en la base de datos. 📤

- Listar pedido: Endpoint para listar todos los productos pedidos. 📥

- Buscar pedido por ID: Endpoint para buscar un pedido específico por
su ID. 📥

- Actualizar pedido: Endpoint para actualizar la información de un pedido
existente. 📤

- Eliminar pedido: Endpoint para eliminar un pedido de la plataforma. 📤