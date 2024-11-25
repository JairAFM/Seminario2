<template>
  <div class="reservation-container">
    <div class="toolbar">
      <v-btn
        v-if="usuario === 0"
        @click="toggleEditMode"
        :color="isEditMode ? 'error' : 'primary'"
        class="edit-button"
      >
        <v-icon left>{{ isEditMode ? 'mdi-check' : 'mdi-pencil' }}</v-icon>
        {{ isEditMode ? 'Finalizar Edición' : 'Modo Edición' }}
      </v-btn>
    </div>

    <div class="main-content">
      <div class="image-container" ref="imageContainer">
        <div
          v-for="img in images"
          :key="img.id"
          class="draggable-image"
          :class="{ 'selectable': !isEditMode }"
          :style="{ width: img.width + 'px', height: img.height + 'px' }"
          :data-id="img.id"
          @click="handleImageClick(img)"
        >
          <img 
            :src="img.src" 
            :alt="img.name" 
            :style="{ width: img.width + 'px', height: img.height + 'px' }" 
          />
          <!-- Controles de edición -->
          <template v-if="isEditMode">
            <div class="resize-handle" @mousedown.stop="initResize($event, img)"></div>
            <button class="delete-button" @click.stop="removeImage(img.id)">
              <v-icon color="error">mdi-delete</v-icon>
            </button>
          </template>
          
          <!-- Indicador de mesa seleccionable -->
          <div v-else class="table-number">Mesa {{ img.id }}</div>
        </div>
      </div>

      <!-- Panel de mesas disponibles (solo en modo edición) -->
      <v-expand-transition>
        <div v-if="isEditMode" class="external-image-container">
          <div class="section-title">
            <v-icon color="primary" class="mr-2">mdi-table-furniture</v-icon>
            <h2>Mesas Disponibles</h2>
            <v-spacer></v-spacer>
            <span class="helper-text">Arrastra las mesas al plano</span>
          </div>
          
          <div class="external-images-grid">
            <v-hover v-for="externalImg in externalImages" :key="externalImg.id" v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                :class="['external-image', { 'on-hover': isHovering }]"
                @click="duplicateImage(externalImg)"
              >
                <v-img
                  :src="externalImg.src"
                  :alt="externalImg.name"
                  class="image-preview"
                  height="80"
                  contain
                ></v-img>
                <v-card-text class="text-center pa-2">
                  {{ externalImg.name }}
                </v-card-text>
                <v-overlay
                  v-if="isHovering"
                  color="#000"
                  opacity="0.5"
                ></v-overlay>
              </v-card>
            </v-hover>
          </div>
        </div>
      </v-expand-transition>
    </div>

    <!-- Modal de Reserva -->
    <ReservationModal v-if="selectedImage && !isEditMode" @close="selectedImage = null">
      <div class="modal-content">
        <h2>Mesa {{ selectedImage.id }}</h2>
        <div class="modal-buttons">
          <v-btn color="primary" @click="reserve">
            <v-icon left>mdi-calendar-check</v-icon>
            Reservar
          </v-btn>
          <v-btn color="secondary" @click="viewImage">
            <v-icon left>mdi-image</v-icon>
            Ver Fotos
          </v-btn>
        </div>
      </div>
    </ReservationModal>
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
        { id: 1, name: 'Imagen 1', src: "src/assets/images/imagen1.png", width: 50, height: 50 },
        { id: 2, name: 'Imagen 2', src: "src/assets/images/imagen2.png", width: 50 },
        { id: 3, name: 'Imagen 3', src: "src/assets/images/imagen3.png", width: 50 },
        { id: 4, name: 'Imagen 4', src: "src/assets/images/imagen4.png", width: 50 },
        { id: 5, name: 'Imagen 5', src: "src/assets/images/baños.png", width: 50 },
      ],
      selectedImage: null,
    };
  },
  mounted() {
    this.loadState();  // Cargar estado al iniciar la aplicación
    this.initializeDragAndResize();
  },
  methods: {
    handleImageClick(img) {
      if (!this.isEditMode) {
        this.selectedImage = img;
      }
    },

    toggleEditMode() {
      this.isEditMode = !this.isEditMode;
      this.saveState();
      this.initializeDragAndResize();
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

    reserve() {
      // Aquí se debe enviar el número de mesa al formulario de reservación
      this.$router.push({ 
        path: '/resevarForm',
        query: { mesa: this.selectedImage.id } // Envía el ID de la imagen como número de mesa
      });
      this.selectedImage = null; // Cierra el modal
    },
    
    viewImage() {
      this.$router.push({
        path: '/fotos',
        query: { mesaId: this.selectedImage.id }
      });
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
.reservation-container {
  padding: 20px;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.toolbar {
  margin-bottom: 20px;
  padding: 10px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.edit-button {
  text-transform: none;
  font-weight: 500;
}

.main-content {
  display: flex;
  gap: 20px;
  flex-direction: column;
}

.image-container {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  min-height: 500px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: relative;
}

.external-image-container {
  background-color: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.section-title {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e0e0e0;
}

.section-title h2 {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
  font-weight: 500;
}

.external-images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 16px;
  padding: 8px;
}

.external-image {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
}

.external-image.on-hover {
  transform: translateY(-5px);
}

.image-preview {
  background-color: #f5f5f5;
  border-radius: 8px 8px 0 0;
  padding: 8px;
}

.draggable-image {
  position: absolute;
  cursor: move;
  border: 2px solid transparent;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.draggable-image.selectable {
  cursor: pointer !important;
  transition: all 0.3s ease;
}

.draggable-image.selectable:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.table-number {
  position: absolute;
  bottom: -25px;
  left: 50%;
  transform: translateX(-50%);
  background-color: var(--v-primary-base);
  color: white;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 0.875rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.draggable-image.selectable:hover .table-number {
  opacity: 1;
}

/* Estilos para el modo edición */
.resize-handle {
  width: 12px;
  height: 12px;
  background: var(--v-primary-base);
  border-radius: 50%;
  position: absolute;
  right: -6px;
  bottom: -6px;
  cursor: se-resize;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.draggable-image:hover .resize-handle {
  opacity: 1;
}

.delete-button {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: #ff5252;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 0.875rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.draggable-image:hover .delete-button {
  opacity: 1;
}

.delete-button:hover {
  background-color: #ff1744;
}

/* Animaciones */
.v-expand-transition-enter-active,
.v-expand-transition-leave-active {
  transition: all 0.3s ease-out;
}

.v-expand-transition-enter-from,
.v-expand-transition-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Estilos para el modal */
.modal-content {
  padding: 20px;
  text-align: center;
}

.modal-content h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 1.5rem;
}

.modal-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 20px;
}
</style>