<div align="right">
  <a href="MANUAL.md"><img src="https://img.shields.io/badge/EN-555555?style=flat-square" alt="English"></a>
  &nbsp;<img src="https://img.shields.io/badge/ES-1a6fc4?style=flat-square" alt="Español">
</div>

# Manual de uso — AuryApp

Guía completa para el uso diario de la aplicación de gestión del Beach Club.

---

## Acceso

Abre el navegador y entra en la dirección de la app. Introduce tu usuario y contraseña.

> Si introduces mal la contraseña 5 veces seguidas, la cuenta se bloquea durante 1 hora automáticamente.

> La sesión se cierra automáticamente al cerrar el navegador y caduca tras 8 horas de inactividad.

### Crear cuenta nueva

Si no tienes cuenta, pulsa **Crear cuenta nueva** en la pantalla de login. Rellena nombre, apellidos, usuario, correo y contraseña. Al registrarte entras directamente a la app.

> Las cuentas nuevas no tienen permisos de administrador. Un administrador puede elevarlas desde el panel Admin.

El saludo de bienvenida (Buenos días / Buenas tardes / Buenas noches) y el clima se actualizan solos.

---

## Dashboard

La pantalla de inicio muestra un resumen del día:

- **Clima** — Temperatura y estado del tiempo en Valencia (se actualiza cada 30 minutos)
- **Módulos** — Acceso rápido a todas las secciones con el dato más importante de cada una
- **Puntos de venta** — Estado de cada espacio: quién trabaja hoy y progreso de tareas
- **Próximos eventos** — Tabla con los eventos de los próximos días
- **Avisos** — Cumpleaños, vacaciones aprobadas, días sueltos y contratos próximos a vencer

Los módulos del dashboard muestran animaciones con información relevante (notas recientes, trabajadores del día, próximos eventos...). Se actualizan solos cada 10 minutos.

---

## Temas visuales

En la esquina superior derecha, haz clic en tus iniciales para desplegar el menú de usuario. Desde ahí puedes cambiar el tema de la app:

| Tema | Estilo |
|------|--------|
| Claro | Blanco y azul, predeterminado |
| Oscuro | Fondo negro, iconos en azul |
| Mint | Verde menta |
| Barbie | Rosa |
| Drácula | Morado oscuro |
| Cyberpunk | Negro y amarillo |

Tu elección se guarda automáticamente para las próximas visitas.

---

## Agenda

Notas y recordatorios con prioridad. Accede desde el módulo **Agenda** del dashboard.

### Añadir una nota

1. Escribe el texto en el campo de texto
2. Selecciona la prioridad:
   - **Urgente** — aparece siempre arriba, borde rojo
   - **Moderado** — borde amarillo
   - **Normal** — borde verde (por defecto)
3. Pulsa **Añadir nota** o usa `Ctrl + Enter`

### Dictar por voz

Pulsa el icono del micrófono y habla. El texto aparece automáticamente en el campo. Funciona en Chrome y Edge.

### Resolver una nota

Pulsa el icono ✓ en la nota. Desaparece de la lista principal y pasa a la sección **Resueltas recientemente** al fondo, con texto tachado.

### Eliminar una nota

Pulsa el icono de papelera. La nota se elimina sin confirmación.

---

## Eventos

Gestión de celebraciones: bodas, graduaciones, comuniones, galas, prebodas y otros.

### Ver todos los eventos

Accede desde **Eventos** en el dashboard o en el menú.

### Crear un evento

1. Pulsa **Nuevo evento**
2. Rellena: cliente, tipo, concepto, fecha, espacios, número de personas y notas
3. Guarda

### Detalle de un evento

Desde la ficha del evento puedes:

- **Editar** los datos del evento
- **Subir documentos** (PDF, imágenes, presupuestos...)
- **Rangos y camareros** — añadir grupos de trabajo (ej: "Salón principal") y asignar camareros con su función
- **Plano de mesas** — editor visual para diseñar la distribución del espacio

### Plano de mesas (editor visual)

El editor permite diseñar la distribución de mesas y espacios de cada evento.

#### Añadir elementos

Pulsa un botón de la barra de herramientas para entrar en modo colocación — el cursor cambia a **cruz**. Luego haz clic en el canvas donde quieras colocar el elemento. Pulsa `Escape` para cancelar sin colocar nada.

| Elemento | Descripción |
|----------|-------------|
| Mesa redonda | Mesa circular con etiqueta |
| Mesa rectangular | Mesa rectangular con etiqueta |
| Cóctel | Mesa alta de cóctel |
| Escenario | Zona de escenario (único) |
| Barra | Barra del local (única) |
| DJ | Zona de DJ (única) |
| TV | Televisión (única) |
| Altavoz | Altavoz de ambiente |
| Zona | Área con nombre redimensionable (recuadro de color con etiqueta) |
| Columna | Columna estructural |
| Planta | Elemento de decoración vegetal |
| Entrada invitados | Acceso de invitados (único) |
| Salida invitados | Salida de invitados (única) |
| Entrada camareros | Acceso del personal de servicio (único) |
| Salida camareros | Salida del personal de servicio (única) |
| Texto | Texto libre editable |

#### Añadir en lote

Pulsa **Añadir lote** para colocar varias mesas a la vez. Elige el tipo, la cantidad y la disposición:
- **Horizontal** — fila de izquierda a derecha
- **Vertical** — columna de arriba a abajo
- **Círculo** — distribuidas en círculo alrededor del punto donde hagas clic

#### Información de mesa

Haz clic en una mesa para seleccionarla. Se abre el **panel Info** a la derecha con los campos:
- Nombre, rango, número de pax, carne, pescado, vegetariano, infantil, celíacos, alérgicos y notas

El número de pax también se muestra como etiqueta directamente debajo de la mesa en el canvas, actualizado en tiempo real.

Los cambios se guardan al instante al pulsar fuera del campo o al cerrar el panel.

#### Editar todas las mesas

Pulsa **Editar mesas** (desde el detalle del evento) para ver todas las mesas del plano en una tabla. Cada fila tiene los mismos campos que el panel Info del plano. Los cambios se guardan automáticamente fila a fila (sin botón de guardar).

#### Selección múltiple

Mantén `Shift` y haz clic en varios elementos, o arrastra un rectángulo de selección para seleccionar varios a la vez. Con varios elementos seleccionados:
- **Eliminar** (tecla `Supr` o botón papelera) los borra todos a la vez
- **Selector de color** aplica el nuevo color a todos los elementos seleccionados a la vez

#### Etiquetas de entradas y salidas

Las etiquetas de entradas y salidas de invitados y camareros se muestran siempre en horizontal debajo del elemento, independientemente de cómo esté girado.

#### Otras acciones

- **Mover elementos** — arrastra con el dedo (móvil/tablet) o con el ratón
- **Redimensionar** — arrastra las esquinas del objeto seleccionado
- **Cambiar color** — selecciona el objeto y usa el selector de color en la barra superior
- **Renombrar** — doble clic en cualquier elemento para cambiarle el nombre
- **Eliminar** — selecciona y pulsa la tecla `Supr` o el botón de la papelera
- **Deshacer / Rehacer** — botones ↩ ↪ en la barra superior
- **Candado** — activa el modo candado para bloquear los elementos y evitar moverlos sin querer al deslizar
- **Zoom** — pellizca con dos dedos en móvil/tablet o usa la rueda del ratón
- **Guardar** — se guarda automáticamente al modificar cualquier elemento
- **Exportar** — descarga el plano como imagen PNG o PDF (con etiquetas y badges de pax incluidos)

---

## Cuadrante de turnos

Vista semanal de todos los empleados y sus turnos.

### Navegar entre semanas

Usa las flechas **←** **→** para moverte semana a semana.

### Asignar un turno

Haz clic en el día de un empleado y selecciona el tipo de turno.

### Colores de turno

Cada tipo de turno tiene un color distinto en el cuadrante:

| Estado | Color |
|--------|-------|
| Trabajo | Color del empleado (verde por defecto) |
| Libre | Morado |
| Inamovible | Naranja |
| Vacaciones | Amarillo |
| Libre + vacaciones | Naranja claro |
| Fin de semana largo | Lila |
| Baja | Rojo |

### Asignar espacio a un empleado

Desde la ficha del espacio o desde el cuadrante, arrastra el empleado al espacio correspondiente.

---

## Personal

Gestión de la plantilla del club.

### Ficha de empleado

Cada empleado tiene: nombre, apellidos, rol, teléfono, email, fecha de nacimiento, tipo de contrato y fecha de vencimiento (si aplica).

Campos adicionales relevantes para el cuadrante:

- **Color** — color que representa al empleado en el cuadrante cuando trabaja (verde por defecto)
- **Horas semanales** — horas de contrato (40 o 30); se usa para calcular disponibilidad

### Alertas de vencimiento

En el dashboard (sección **Vencimientos**) aparecen los contratos que vencen en los próximos días. Los vencidos aparecen en rojo.

---

## Vacaciones y días sueltos

### Solicitar ausencia (como empleado)

1. Ve a la ficha del empleado
2. Pulsa **Nueva solicitud**
3. Selecciona tipo (vacaciones / día suelto / libre...), fechas y notas opcionales
4. La solicitud queda en estado **Pendiente**

### Aprobar o rechazar (como admin)

Desde **Vacaciones** o **Días sueltos** en el menú, verás todas las solicitudes pendientes con botones para aprobar o rechazar.

Las solicitudes aprobadas aparecen en el dashboard en la sección **Avisos**.

---

## Tareas

Checklists de apertura y cierre por espacio. Se generan automáticamente cada día.

### Marcar una tarea como completada

Haz clic en la tarea. Se marca al instante (sin recargar la página). La barra de progreso del espacio se actualiza en el dashboard.

### Ver tareas de un espacio

Accede desde **Puntos de venta** en el dashboard o desde **Espacios** en el menú.

---

## Pedidos

Registro de artículos necesarios por punto de venta.

### Añadir un artículo

1. Entra en el espacio desde **Pedidos**
2. Pulsa **Nuevo artículo**
3. Introduce nombre y cantidad

### Actualizar cantidad

Usa los botones **+** y **−** directamente en la lista. Se guarda al instante.

---

## Calendario

Vista mensual de todos los eventos. Navega con las flechas del mes. Haz clic en un evento para ver su detalle.

---

## Panel de administración

Si tu cuenta tiene permisos de staff, aparece el botón **Admin** (con icono de escudo) en la barra superior. Desde ahí puedes gestionar usuarios, grupos y todos los modelos de la app directamente.

---

## Cerrar sesión

Haz clic en tus iniciales (esquina superior derecha) y pulsa **Cerrar sesión**.

---

## Soporte

Desarrollado por **Fernando Vilas Paz**  
[GitHub](https://github.com/fvilpaz) · [LinkedIn](https://www.linkedin.com/in/fernando-vilas-paz-1626901a9)
