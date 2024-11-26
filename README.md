# Image Generator and Editor

## Descripción

Este proyecto es una aplicación interactiva diseñada para generar y editar imágenes utilizando APIs como Ideogram y OpenAI. Su funcionamiento está basado en el contexto proporcionado por el usuario, permitiendo tomar decisiones dinámicas sobre la generación y edición de imágenes. Además, recuerda las imágenes generadas previamente o las proporcionadas por el usuario para un flujo continuo e intuitivo.

---

## Funcionalidades

1. **Generación de Imágenes**:

   - Permite a los usuarios crear imágenes a partir de descripciones (_prompts_).
   - Utiliza parámetros opcionales como estilo, modelo, relación de aspecto, entre otros, para personalizar los resultados.
   - La imagen generada se guarda en el contexto para futuras acciones.

2. **Edición de Imágenes**:

   - El usuario puede editar imágenes generadas previamente o proporcionadas a través de una URL.
   - Se genera automáticamente una máscara blanca que cubre toda la imagen, lo que permite modificaciones completas.
   - Permite aplicar estilos y ajustes personalizados según las necesidades del usuario.

3. **Gestión de Contexto**:

   - La aplicación almacena:
     - **Última imagen generada:** Imagen creada por la aplicación.
     - **Última imagen proporcionada:** Imagen enviada manualmente por el usuario.
   - Este contexto permite editar imágenes de manera dinámica, ya sea la última generada o la última proporcionada.

4. **Historial Interactivo**:
   - Se muestra un registro de las acciones realizadas, permitiendo al usuario revisar el flujo de la conversación.

---

## Flujo de Decisiones

![Descripción del diagrama](assets/diagrama.jpeg)

### 1. Entrada del Usuario

- El usuario describe lo que desea realizar: generar, editar o hacer preguntas.
- Si el texto incluye una URL válida, esta se detecta y almacena en el contexto como la última imagen proporcionada.

### 2. Análisis de la Solicitud

- La aplicación utiliza un modelo para decidir si el usuario desea:
  - **Generar una nueva imagen.**
  - **Editar una imagen existente.**
  - **No realizar ninguna acción.**

### 3. Generación de Imagen

- Si se decide generar una imagen:
  - Se construye una solicitud con los parámetros proporcionados por el usuario.
  - La imagen generada se guarda en el contexto como la última imagen generada.
  - Se muestra al usuario la URL de la imagen creada.

### 4. Edición de Imagen

- Si se decide editar una imagen:
  - Se selecciona automáticamente una imagen del contexto:
    - Si el usuario proporcionó una URL, esta tiene prioridad.
    - Si no, se utiliza la última imagen generada por la aplicación.
  - Se genera una máscara blanca para cubrir toda la imagen.
  - Se envía la solicitud de edición a la API con los parámetros definidos.
  - La nueva imagen editada se guarda en el contexto como la última imagen generada.

### 5. Confirmación de Parámetros

- Antes de realizar cualquier acción, se presentan los parámetros al usuario.
- El usuario puede confirmar los parámetros o editarlos antes de proceder.

---

## Estructura del Flujo

1. **Inicio**:

   - El usuario proporciona su solicitud inicial.
   - Si incluye una URL, esta se guarda automáticamente en el contexto.

2. **Decisión**:

   - Se analiza la solicitud para determinar si es una acción de generación, edición o una consulta general.

3. **Ejecución de Acción**:

   - **Generar**:
     - Se crea una nueva imagen basada en el _prompt_ y los parámetros opcionales.
   - **Editar**:
     - Se utiliza una imagen del contexto (proporcionada o generada previamente).
     - Se genera una máscara y se envía la solicitud de edición.
   - **Ninguna Acción**:
     - Se continúa con la conversación sin realizar ninguna operación.

4. **Historial y Contexto**:
   - Se registra cada acción en un historial interactivo.
   - Las imágenes generadas o editadas se guardan en el contexto para futuras referencias.

---

## Características Clave

1. **Detección de URL de Imágenes**:

   - Analiza la entrada del usuario para identificar si incluye una URL válida.
   - Las URLs detectadas se almacenan como la última imagen proporcionada.

2. **Máscara Automática**:

   - Genera una máscara completamente blanca que cubre toda la imagen original.
   - Permite realizar ediciones completas sin necesidad de intervención manual.

3. **Persistencia de Contexto**:

   - Recuerda las imágenes utilizadas previamente, permitiendo flujos continuos y acciones dependientes del historial.

4. **Confirmación de Parámetros**:

   - El usuario puede revisar y ajustar los parámetros antes de ejecutar cualquier acción.

5. **Gestión Automática de Archivos Temporales**:
   - Las imágenes descargadas y las máscaras generadas se eliminan automáticamente después de cada operación.

---

## Ejemplo de Uso

### Generación de Imagen

**Usuario:**  
"Quiero un gato sobre una mesa de billar."

**Sistema:**  
"Se determinó que se debe generar una imagen.  
Prompt: un gato sobre una mesa de billar.  
¿Deseas proceder a generar la imagen con estos parámetros? (s/n)"

**Resultado:**  
Se genera la imagen y se guarda en el contexto.

---

### Edición de Imagen

**Usuario:**  
"Quiero que el gato sea naranja."

**Sistema:**  
"Se determinó que se debe editar una imagen.  
Prompt: Cambiar el color del gato a naranja.  
Imagen utilizada: URL de la última imagen generada.  
¿Deseas proceder a editar la imagen con estos parámetros? (s/n)"

**Resultado:**  
La imagen es editada y la nueva versión se guarda en el contexto.

---

## Requisitos del Proyecto

1. **Dependencias**:

   - Instale las dependencias utilizando el siguiente comando:
     ```bash
     pip install -r requirements.txt
     ```

2. **Variables de Entorno**:
   - Cree un archivo `.env` con las siguientes variables:
     ```plaintext
     IDEOGRAM_API_KEY=<your_ideogram_api_key>
     OPENAI_API_KEY=<your_openai_api_key>
     ```
