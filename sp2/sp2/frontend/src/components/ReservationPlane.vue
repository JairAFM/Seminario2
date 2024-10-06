<template>
  <div>
    <div class="toolbar">
      <button v-if="usuario === 0" @click="toggleEditMode">
        {{ isEditMode ? 'Listo' : 'Editar' }}
      </button>
    </div>
    <div class="image-container" ref="imageContainer">
      <div
        v-for="img in images"
        :key="img.id"
        class="draggable-image"
        :style="{ width: img.width + 'px', height: img.height + 'px' }"
        :data-id="img.id"
        @click="selectImage(img)"
        @mousedown.prevent="initResize($event, img)"
      >
        <img :src="img.src" :alt="img.name" :style="{ width: img.width + 'px', height: img.height + 'px' }" />
        <div class="resize-handle" @mousedown.stop="initResize($event, img)"></div>
        <button v-if="isEditMode" class="delete-button" @click.stop="removeImage(img.id)">Eliminar</button>
      </div>
    </div>

    <div class="external-image-container" v-if="usuario === 0">
      <div
        v-for="externalImg in externalImages"
        :key="externalImg.id"
        class="external-image"
        @click="duplicateImage(externalImg)"
      >
        <img :src="externalImg.src" :alt="externalImg.name" style="height: 60px; width: 60px;" />
      </div>
    </div>
    
    <modal v-if="selectedImage" @close="selectedImage = null">
      <h3>{{ selectedImage.name }}</h3>
      <button @click="reserve">Reservar</button>
      <button @click="viewImage">Ver vista</button>
    </modal>

    <!-- Aquí se renderizará el contenido de las rutas -->
    <router-view></router-view>
  </div>
</template>

<script>
import interact from 'interactjs';
import Modal from './ReservationModal.vue'; 

export default {
  components: {
    Modal,
  },
  data() {
    return {
      isEditMode: true,
      usuario: 0, // Cambia el valor aquí según sea necesario
      images: [],
      externalImages: [
        { id: 1, name: 'Imagen 1', src: "http://localhost:5000/static/imagen1.png", width: 50, height: 50 },
        { id: 2, name: 'Imagen 2', src: "http://localhost:5000/static/imagen2.png", width: 50 },
        { id: 3, name: 'Imagen 3', src: "http://localhost:5000/static/imagen3.png", width: 50 },
        { id: 4, name: 'Imagen 4', src: "http://localhost:5000/static/imagen4.png", width: 50 },
        { id: 5, name: 'Imagen 5', src: "http://localhost:5000/static/baños.png", width: 50 },
      ],
      selectedImage: null,
    };
  },
  mounted() {
    this.loadState();  // Cargar estado al iniciar la aplicación
    this.initializeDragAndResize();
  },
  methods: {
    toggleEditMode() {
      this.isEditMode = !this.isEditMode;
      this.saveState(); // Guardar el estado actual al cambiar el modo
      this.initializeDragAndResize(); // Re-inicializar después de cambiar el modo
    },

    initializeDragAndResize() {
      interact('.draggable-image')
        .draggable({
          inertia: true,
          modifiers: [
            interact.modifiers.restrictRect({
              restriction: 'parent',
            }),
          ],
          autoScroll: true,
          onmove: this.dragMoveListener,
          enabled: this.isEditMode, // Desactivar arrastre si no está en modo edición
        })
        .resizable({
          edges: { right: true, bottom: true },
          modifiers: [
            interact.modifiers.restrictSize({
              min: { width: 50, height: 50 },
            }),
          ],
          enabled: this.isEditMode, // Desactivar redimensionamiento si no está en modo edición
          listeners: {
            move: (event) => this.resizeMove(event),
          },
        });
    },

    dragMoveListener(event) {
      const target = event.target;

      // Mantiene la posición actual
      const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
      const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

      // Traslada el elemento
      target.style.transform = `translate(${x}px, ${y}px)`;

      // Actualiza la posición
      target.setAttribute('data-x', x);
      target.setAttribute('data-y', y);

      // Actualiza las propiedades de la imagen
      const img = this.images.find(image => image.id == target.dataset.id);
      if (img) {
        img.x = x; // Guardar la nueva posición x
        img.y = y; // Guardar la nueva posición y
      }

      this.saveState(); // Guardar estado cuando se mueva una imagen
    },

    selectImage(image) {
      if (!this.isEditMode) {
        this.selectedImage = image;
      }
    },

    reserve() {
      // Aquí se debe enviar el número de mesa al formulario de reservación
      this.$router.push({ 
        path: '/reserve',
        query: { mesa: this.selectedImage.id } // Envía el ID de la imagen como número de mesa
      });
      this.selectedImage = null; // Cierra el modal
    },
    
    viewImage() {
      this.$router.push('/fotos');
    },

    duplicateImage(externalImg) {
      const newImg = {
        id: this.images.length + 1,
        name: externalImg.name,
        src: externalImg.src,
        width: 100, // Tamaño inicial
        height: 100,
        x: 0, // Establecer posición inicial
        y: 0, // Establecer posición inicial
      };
      this.images.push(newImg);
      this.saveState(); // Guardar estado al duplicar una imagen
    },

    removeImage(id) {
      this.images = this.images.filter(img => img.id !== id);
      this.saveState(); // Guardar estado al eliminar una imagen
    },

    resizeMove(event) {
      if (!this.isEditMode) return; // No hacer nada si no está en modo edición

      const target = event.target;
      const img = this.images.find(image => image.id == target.dataset.id);

      if (img) {
        // Actualiza el tamaño de la imagen
        img.width += event.deltaRect.width;
        img.height += event.deltaRect.height;

        // Actualiza el estilo de la imagen
        target.style.width = `${img.width}px`;
        target.style.height = `${img.height}px`;

        // Establece el nuevo tamaño de la imagen interna
        const imageElement = target.querySelector('img');
        if (imageElement) {
          imageElement.style.width = `${img.width}px`;
          imageElement.style.height = `${img.height}px`;
        }

        this.saveState(); // Guardar estado al redimensionar una imagen
      }
    },

    initResize(event, img) {
      if (!event || !img) {
        console.error("El evento o la imagen no están definidos");
        return;
      }
      event.preventDefault(); // Evita que se seleccione el texto
    },

    // Guardar el estado en localStorage
    saveState() {
      const state = {
        isEditMode: this.isEditMode,
        images: this.images.map(image => ({
          id: image.id,
          name: image.name,
          src: image.src,
          width: image.width,
          height: image.height,
          x: parseFloat(image.x) || 0, // Guardar la posición x
          y: parseFloat(image.y) || 0  // Guardar la posición y
        })),
      };
      localStorage.setItem('appState', JSON.stringify(state));
    },

    // Cargar el estado desde localStorage
    loadState() {
      const savedState = localStorage.getItem('appState');
      if (savedState) {
        const state = JSON.parse(savedState);
        this.isEditMode = state.isEditMode;
        this.images = state.images.map(image => ({
          id: image.id,
          name: image.name,
          src: image.src,
          width: image.width,
          height: image.height,
          x: image.x, // Asegúrate de restaurar la posición x
          y: image.y  // Asegúrate de restaurar la posición y
        }));
        this.$nextTick(() => {
          this.images.forEach((img) => {
            const imgElement = this.$refs.imageContainer.querySelector(`.draggable-image[data-id="${img.id}"]`);
            if (imgElement) {
              imgElement.style.transform = `translate(${img.x}px, ${img.y}px)`; // Restaurar la posición
              imgElement.setAttribute('data-x', img.x); // Actualizar el atributo de posición
              imgElement.setAttribute('data-y', img.y); // Actualizar el atributo de posición
            }
          });
        });
      }
    },
  },
};
</script>

<style scoped>
.image-container {
  position: relative;
  width: 100%;
  height: 500px; /* Ajusta el tamaño según sea necesario */
  border: 1px solid #ccc;
}

.draggable-image {
  position: absolute;
  cursor: move;
  border: 1px solid #ccc;
  margin: 10px;
}

.resize-handle {
  width: 10px;
  height: 10px;
  background: red;
  position: absolute;
  right: 0;
  bottom: 0;
  cursor: se-resize;
}

.delete-button {
  position: absolute;
  top: 5px;
  right: 5px;
}
</style>
