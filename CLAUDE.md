# AuryApp — Guía para Claude

Guía de referencia para trabajar en este proyecto sin romper lo que ya funciona.
**Leer completa antes de tocar cualquier archivo. Sin excepciones.**

---

## Protocolo obligatorio ante cualquier cambio

Antes de escribir una sola línea de código, hacer siempre este análisis en orden:

### 1. Entender qué se pide
- ¿Qué quiere el usuario exactamente? No asumir, no interpretar de más.
- Si hay ambigüedad, preguntar antes de implementar.
- Confirmar el entendimiento con el usuario antes de actuar si el cambio es grande.

### 2. Identificar qué archivos están implicados
- ¿Qué vista(s) de Django afecta?
- ¿Qué template(s) afecta?
- ¿Qué URL(s) afecta?
- ¿Qué modelos afecta? (¿Necesita migración?)
- ¿Qué JS afecta?

### 3. Analizar impacto — preguntas obligatorias

| Pregunta | Por qué importa |
|----------|----------------|
| ¿Qué otras partes del código llaman a lo que voy a cambiar? | Romper una función/endpoint rompe todo lo que depende de él |
| ¿Este cambio toca datos en BD? | Puede corromper datos existentes |
| ¿Este cambio toca el canvas Fabric.js? | El canvas es frágil — ver sección específica |
| ¿Este cambio toca `guardar_plano` o `guardar_info_mesa`? | La arquitectura de guardado es delicada — ver sección específica |
| ¿Este cambio toca CSS? | Las clases `bc-*` se usan en múltiples templates |
| ¿Este cambio añade un nuevo endpoint? | Hay que añadirlo también en `urls.py` |

### 4. Buscar usos antes de renombrar o eliminar
Antes de renombrar una función, clase, endpoint o variable:
```bash
grep -r "nombre_a_cambiar" --include="*.py" --include="*.html" --include="*.js" .
```
Si aparece en más de un sitio, cambiar TODOS o no cambiar nada.

### 5. Hacer un cambio mínimo
- Cambiar solo lo necesario para resolver el problema.
- No aprovechar para "limpiar" o "mejorar" código adyacente que no se pidió.
- Si hay que tocar 5 archivos para algo simple, probablemente el enfoque es incorrecto.

### 6. Verificar que nada se rompió
- ¿Siguen existiendo todas las rutas de URL que existían antes?
- ¿Siguen funcionando las funciones JS que llamaban a lo que se cambió?
- ¿El template puede resolver todos los `{% url %}` que usa?

---

## Stack

- **Backend**: Django 6.x · Python 3.12 · SQLite (local) / Neon PostgreSQL (producción)
- **Frontend**: Fabric.js 5.3.1 (canvas interactivo) · CSS propio (clases `bc-*`)
- **Infra**: Google Cloud Run · proyecto `auryapp-prod` · región `europe-west1` · dominio `aury-op.com`
- **Deploy**: `bash deploy.sh` — sube el directorio actual con `gcloud run deploy --source .`
- **Migraciones en prod**: `DATABASE_URL="..." ~/.pyenv/versions/3.12.12/bin/python manage.py migrate`

---

## Mapa de archivos clave

| Archivo | Qué hace | Depende de |
|---------|----------|------------|
| `core/views.py` | Vistas: eventos, plano, editar_mesas, guardar_plano, guardar_info_mesa | models.py, todos los templates de core |
| `core/urls.py` | URLs del módulo core | views.py — cada URL apunta a una vista |
| `core/models.py` | Evento, Espacio, EventoRango, EventoCamarero | migraciones en `core/migrations/` |
| `core/templates/core/detalle_evento.html` | Plano Fabric.js — TODA la lógica del canvas está aquí | guardar_plano, guardar_info_mesa, editar_mesas, resumen_mesas |
| `core/templates/core/editar_mesas.html` | Tabla de mesas con autosave | guardar_info_mesa (AJAX directo) |
| `core/templates/core/resumen_mesas.html` | Vista solo lectura del resumen | plano_json de la BD |
| `personal/models.py` | Empleado (color, horas_semana), Turno (color_override) | migraciones en `personal/migrations/` |
| `personal/views.py` | Cuadrante, turnos, empleados | personal/models.py |
| `beachclub/urls.py` | URLs raíz (logout, robots.txt, includes) | core/urls.py, personal/urls.py |
| `deploy.sh` | Deploy a Cloud Run | .env.deploy (no commitear) |

---

## Sistema de plano (Fabric.js)

### Patrón para añadir un nuevo tipo de elemento

Todos los cambios van en `core/templates/core/detalle_evento.html`. Checklist obligatorio:

1. **`COLOR_DEFECTO`** — `'nuevo-tipo': '#hexcolor'`
2. **`BASE_NOMBRE`** — `'nuevo-tipo': 'Nombre base'` (vacío `''` si sin etiqueta)
3. **`TIPO_UNICO`** — añadir si solo puede haber uno en el canvas
4. **`crearGrupo(tipo, etiqueta, color)`** — rama `else if` con la geometría
   - Siempre terminar: `return new fabric.Group(objs, { left: gx, top: gy, _tipo: tipo, _etiqueta: etiqueta });`
   - Objeto principal: `obj._main = true`
5. **Botón toolbar** — `<button class="bc-btn bc-btn-sm" data-add="nuevo-tipo">` en el grupo HTML correcto
6. **`LOTE_TAMS`** (opcional) — solo si debe estar en "añadir en lote"

### Tipos existentes — NO reutilizar estos nombres

| `_tipo` | Color | `TIPO_UNICO` | Notas |
|---------|-------|-------------|-------|
| `mesa-redonda` | #3b82f6 | no | tiene `_info` |
| `mesa-rect` | #3b82f6 | no | tiene `_info` |
| `coctel` | #3b82f6 | no | tiene `_info` |
| `escenario` | #8b5cf6 | sí | |
| `barra` | #f59e0b | sí | |
| `zona` | #10b981 | no | Textbox nativo |
| `dj` | #f97316 | sí | |
| `tv` | #1e3a5f | sí | |
| `altavoz` | #64748b | no | |
| `columna` | #374151 | no | sin etiqueta |
| `planta` | #16a34a | no | sin etiqueta |
| `entrada` | #10b981 | sí | Entrada invitados |
| `salida` | #ef4444 | sí | Salida invitados |
| `entrada-cam` | #f97316 | sí | Entrada camareros |
| `salida-cam` | #1e40af | sí | Salida camareros |
| `texto` | #111827 | sí | IText editable |

### Reglas críticas del canvas

**`MESA_TIPOS = ['mesa-redonda', 'mesa-rect', 'coctel']`** — NUNCA añadir otros tipos. Determina qué objetos tienen `_info` y aparecen en editar_mesas/resumen_mesas.

**`EXTRA_PROPS = ['_tipo','_etiqueta','_color','_main','_info']`** — Si se añade una propiedad custom nueva, añadirla aquí también para que Fabric.js la serialice.

**`snapshot()`** — Llamar siempre después de modificar el canvas. Gestiona undo/redo y programa el autosave.

---

## Sistema de guardado de datos de mesa (_info)

### Arquitectura — no cambiar sin entender esto

Hay dos responsabilidades completamente separadas:

| Responsabilidad | Endpoint | Quién lo llama |
|----------------|----------|----------------|
| Estructura canvas (posiciones, colores, nombres) | `guardar_plano` `/eventos/<pk>/plano/guardar/` | Autosave canvas, `guardarYNavegar` |
| Datos de mesa (pax, carne, pescado, alergias…) | `guardar_info_mesa` `/eventos/<pk>/plano/guardar_info/` | Panel Info, editar_mesas |

**`guardar_plano` NUNCA modifica `_info`** — preserva siempre el `_info` de la BD.

**`guardar_info_mesa`** es el único sitio que actualiza `_info`. También puede renombrar una mesa.

**`editar_mesas`** llama directamente a `guardar_info_mesa` fila a fila (AJAX). Mismo endpoint que el panel Info del plano.

```
Panel Info (plano) ──────┐
                          ├──► guardar_info_mesa ──► _info en BD
editar_mesas (AJAX) ─────┘

Canvas autosave ──────────► guardar_plano ──► estructura en BD (preserva _info)
```

### Por qué existe esta separación

Fabric.js no restaura propiedades custom (`_info`) en grupos al hacer `loadFromJSON`. Si `guardar_plano` pudiera sobreescribir `_info`, los datos de pax/carne/pescado se perderían cada vez que el canvas se guarda. Romper esta separación vuelve a introducir ese bug.

---

## CSS — design system `bc-*`

Antes de añadir un estilo nuevo, buscar si ya existe. Clases frecuentes:

- **Botones**: `bc-btn bc-btn-primary / bc-btn-secondary / bc-btn-danger / bc-btn-sm / bc-btn-xs`
- **Layout**: `bc-section / bc-section-header / bc-section-body / bc-card / bc-grid-auto`
- **Flex**: `bc-flex / bc-gap-8 / bc-flex-center / bc-ml-auto / bc-shrink-0`
- **Tabla**: `bc-table / bc-table-wrapper`
- **Tipografía**: `bc-text-muted / bc-text-sm / bc-text-xs / bc-font-medium`
- **Formularios**: `bc-form-group / bc-editar-input / bc-editar-input-num / bc-editar-input-notas`

---

## Convenciones de nombres — seguir siempre lo existente

| Contexto | Convención | Ejemplo |
|----------|------------|---------|
| Vistas Django | snake_case, verbo en español | `guardar_plano`, `editar_mesas` |
| URLs (path) | kebab-case | `/plano/guardar/`, `/mesas/editar/` |
| Nombres de URL (name=) | snake_case | `guardar_plano`, `editar_mesas` |
| Variables JS | camelCase | `guardarPlano`, `infoTarget` |
| Tipos canvas `_tipo` | kebab-case | `mesa-redonda`, `entrada-cam` |
| Clases CSS | prefijo `bc-`, kebab-case | `bc-plano-toolbar` |
| Templates | snake_case | `detalle_evento.html` |

---

## Cambios en modelos Django

1. Editar el modelo en `models.py`
2. `python manage.py makemigrations`
3. `python manage.py migrate` (local)
4. En producción: `DATABASE_URL="..." ~/.pyenv/versions/3.12.12/bin/python manage.py migrate`
5. Campos nuevos: siempre `default=` o `null=True` para no romper filas existentes

---

## Módulo personal (empleados y turnos)

- **Colores de estado** en `ESTADO_COLORES` (`personal/models.py`): `libre`=#7030a0, `inamovible`=#ff9300, `vacaciones`=#ffc000, `libre_vacaciones`=#f97316, `finde_largo`=#a855f7, `baja`=#ff0000
- **Color de trabajo**: usa `empleado.color` (verde #16a34a por defecto, rosa #ec4899 para Inma)
- **`horas_semana`**: horas de contrato (40 o 30), no horas calculadas
- **Orden cuadrante**: campo `posicion` en `Empleado`

---

## Deploy

```bash
bash deploy.sh
```

Usa `gcloud run deploy --source .` — despliega el directorio actual, no requiere commit. Variables de entorno desde `.env.deploy` (no commitear, en `.gitignore`).

---

## Historial de decisiones importantes

| Decisión | Motivo |
|----------|--------|
| `guardar_plano` no toca `_info` | Fabric.js no restaura props custom en grupos → los datos de menú se perdían en cada autosave |
| `guardar_info_mesa` endpoint separado | Única forma fiable de persistir `_info` sin depender de la serialización de Fabric.js |
| `editar_mesas` sin botón de guardar, AJAX por fila | Mismo mecanismo que el panel Info del plano — consistencia y fiabilidad |
| `TIPO_UNICO` para entradas/salidas | Solo tiene sentido una entrada de invitados y una de camareros en el plano |
| `object:modified` corrige distorsión de texto | Al escalar un grupo no uniformemente, el texto interno se estiraba — se corrige con escala geométrica media |
