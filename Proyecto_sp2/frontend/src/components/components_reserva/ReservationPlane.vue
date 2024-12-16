<template>
  <div class="reservation-container">
    <div class="toolbar">
      <v-btn
        v-if="usuario == 0"
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
          :class="{ 'selectable': !isEditMode && img.capacidad > 0 }"
          :style="{ width: img.width + 'px', height: img.height + 'px' }"
          :data-id="img.id"
          @click="!isEditMode && img.capacidad > 0 ? handleImageClick(img) : null"
        >
          <img 
            :src="img.src" 
            :alt="img.name" 
            :style="{ width: img.width + 'px', height: img.height + 'px' }" 
          />
          <!-- Controles de edición -->
          <template v-if="isEditMode">
            <div class="resize-handle" @mousedown.stop="initResize($event, img)"></div>
            <div class="button-container">
              <button class="action-button delete-button" @click.stop="eliminarMesaLista(img.id)">
                <v-icon color="white">mdi-delete</v-icon>
              </button>
              <button class="action-button manage-capacity-button" @click.stop="cambiarCapacidad(img.id)">
                <v-icon color="white">mdi-pencil</v-icon>
              </button>
              <button class="action-button add-image-button" @click.stop="addImagen(img.id)">
                <v-icon color="white">mdi-camera-plus</v-icon>
              </button>
            </div>
          </template>
          
          <!-- Indicador de mesa seleccionable -->
          <div v-else class="table-number" style="display: none;">Mesa {{ img.id }}</div>
        </div>
      </div>

      <!-- Panel de mesas disponibles (solo en modo edición) -->
      <v-expand-transition>
        <div v-if="isEditMode" class="external-image-container">
          <div class="section-title">
            <v-icon color="primary" class="mr-2">mdi-table-furniture</v-icon>
            <h2>Mesas Disponibles</h2>
            <v-spacer></v-spacer>
            <span class="helper-text">Seleccione una imagen</span>
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
import Swal from 'sweetalert2'

export default {
  components: {
    Modal,
  },
  data() {
    return {
      isEditMode: false,
      usuario: 0, 
      images: [],
      externalImages: [
        { num_mesa: 1, capacidad: 2, name: 'Imagen 1', src: "src/assets/images/mesa2.png", width: 50, height: 50 },
        { num_mesa: 2, capacidad: 3, name: 'Imagen 2', src: "src/assets/images/mesa3.png", width: 50 },
        { num_mesa: 3, capacidad: 4, name: 'Imagen 3', src: "src/assets/images/mesa4.png", width: 50 },
        { num_mesa: 4, capacidad: 5, name: 'Imagen 4', src: "src/assets/images/mesa5.png", width: 50 },
        { num_mesa: 5, capacidad: 6, name: 'Imagen 5', src: "src/assets/images/mesa6.png", width: 50 },
        { num_mesa: 6, capacidad: 8, name: 'Imagen 6', src: "src/assets/images/mesa8.png", width: 50 },
        { num_mesa: 7, capacidad: 0, name: 'Imagen 7', src: "src/assets/images/baño.png", width: 50 },
      ],
      selectedImage: null,
      mesasAgregadas: [],
      idArray: [],
      idUpdate: [],
      idNew: [],
      idDelete: [],
      mesasObtenidas: []
    };
  },
  mounted() {
    this.initializeDragAndResize();
    this.isAuthenticated();
    this.obtenerIds();
    this.obtenerMesas();
  },
  methods: {
    isAuthenticated() {
      this.usuario = localStorage.getItem('tipoUser');
    },
    handleImageClick(img) {
      if (!this.isEditMode) {
        this.selectedImage = img;
      }
    },
    async obtenerIds(){
      const obtenerIds = await fetch('http://127.0.0.1:5000/checkMesa', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (obtenerIds.ok) {
        const data = await obtenerIds.json(); 
        this.idArray = data.ids; 
        console.log("Array de IDs: ", this.idArray); 
      } else {
        console.error("Error al obtener los IDs de las mesas");
      }
    },
    async obtenerMesas(){
      const mesasO = await fetch('http://127.0.0.1:5000/getMesas', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (mesasO.ok) {
        const data = await mesasO.json(); 
        this.mesasObtenidas = data; 
        this.mesasAgregadas = [];
        this.mesasAgregadas = data.map(mesa => {
          return {
            id: mesa.id,
            capacidad: mesa.capacidad,
            imagenes: mesa.imagenes ? JSON.stringify({
              nombre: mesa.imagenes.nombre,
              base64: mesa.imagenes.base64
            }) : null,
            posicion_x: mesa.posicion_x,
            posicion_y: mesa.posicion_y,
            num_mesa: mesa.num_mesa
          };
        });

        this.$nextTick(() => {
          this.mesasAgregadas.forEach(mesa => {
            const externalImage = this.externalImages.find(
              img => img.num_mesa === mesa.num_mesa
            );

            if (externalImage) {
              const newImg = {
                id: mesa.id,
                name: externalImage.name,
                src: externalImage.src,
                width: 165,
                height: 165,
                x: mesa.posicion_x,
                y: mesa.posicion_y,
                capacidad: externalImage.capacidad,
                num_mesa: mesa.num_mesa
              };

              this.images.push(newImg);

              this.$nextTick(() => {
                const imgElement = this.$refs.imageContainer.querySelector(`.draggable-image[data-id="${newImg.id}"]`);
                if (imgElement) {
                  imgElement.style.transform = `translate(${mesa.posicion_x}px, ${mesa.posicion_y}px)`;
                  imgElement.setAttribute('data-x', mesa.posicion_x);
                  imgElement.setAttribute('data-y', mesa.posicion_y);
                }
              });
            }
          });
        });

        /*console.log("Array de Mesas: ", this.mesasObtenidas);
        console.log("Mesas Agregadas: ", this.mesasAgregadas);*/
      } else {
        console.error("Error al obtener las mesas");
      }
    },
    async actualizarMesas(mesasData) {
      try {
        const promises = mesasData.map(mesa =>
          fetch(`http://127.0.0.1:5000/editMesa/${mesa.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              capacidad: mesa.capacidad,
              posicion_x: mesa.posicion_x,
              posicion_y: mesa.posicion_y,
              imagenes: mesa.imagenes,
              num_mesa: mesa.num_mesa
            })
          })
        );

        const results = await Promise.all(promises);

        const allSuccessful = results.every(response => response.ok);

        if (!allSuccessful) {
          console.log("error");
        }
      } catch (error) {
        console.log("error");
      }
    },
    async agregarMesa(mesasData) {
      try {
        for(let k = 0; k < mesasData.length; k++){
          for(let m = 0; m < this.mesasAgregadas.length; m++){
            if (mesasData[k] == this.mesasAgregadas[m].id) {
              const mesa = this.mesasAgregadas[m];
              const response = await fetch(`http://127.0.0.1:5000/newMesa`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  id: mesa.id, 
                  capacidad: mesa.capacidad,
                  posicion_x: mesa.posicion_x,
                  posicion_y: mesa.posicion_y,
                  imagenes: mesa.imagenes,
                  num_mesa: mesa.num_mesa
                })
              });

              const results = await Promise.all(response);

              const allSuccessful = results.every(response => response.ok);

              if (allSuccessful) {
                console.log("exitoso");
              } else {
                console.log("error");
              }
            }
          }
        }
      } catch (error) {
        console.log("error");
      }
    },
    async eliminarMesas(mesasData) {

      try {
        for (let k = 0; k < mesasData.length; k++) {
          const mesaId = mesasData[k];
          const promises = mesasData.map(mesa => 
            fetch(`http://127.0.0.1:5000/deleteMesa/${mesaId}`, {
              method: 'DELETE',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
              })
            })
          );

          const results = await Promise.all(promises);
          const allSuccessful = results.every(response => response.ok);
          if (!allSuccessful) {
            throw new Error('Algunas mesas no pudieron ser eliminadas');
          } else {
            console.log("kk " + deletedIds + " mmm " + mesaId);
          }
        }
      } catch (error) {
        console.log("error");
      }
    },
    async toggleEditMode() {
      if (this.isEditMode) {  

        for (const img of this.images) {
          const element = this.$refs.imageContainer.querySelector(`.draggable-image[data-id="${img.id}"]`);
          if (element) {
            const x = parseFloat(element.getAttribute('data-x')) || 0;
            const y = parseFloat(element.getAttribute('data-y')) || 0;
            
            try {
              
              const mesaData = {
                id_mesa: img.id,
                capacidad: img.capacidad,
                posicion_x: Math.round(x),
                posicion_y: Math.round(y),
                imagenes: null,
                num_mesa: img.num_mesa
              };

              // Se actualiza la imagen si se selecciona una
              if (img.uploadedImage) {
                mesaData.imagenes = JSON.stringify({
                  nombre: img.uploadedImage.name,
                  base64: img.uploadedImage.base64
                });
              }

              function addIfNotExists(array, value) {
                if (!array.includes(value)) {
                  array.push(value);
                }
              }

              for (let i = 0; i < this.idArray.length; i++) {
                const idArrayItem = this.idArray[i];
                const matchingMesa = this.mesasAgregadas.find(mesa => mesa.id === idArrayItem);

                if (matchingMesa) {
                  addIfNotExists(this.idUpdate, matchingMesa); 
                } else {
                  addIfNotExists(this.idDelete, idArrayItem); 
                }
              }

              for (let j = 0; j < this.mesasAgregadas.length; j++) {
                const mesasAgregadasItem = this.mesasAgregadas[j].id;
                const existsInIdArray = this.idArray.includes(mesasAgregadasItem);

                if (!existsInIdArray) {
                  addIfNotExists(this.idNew, mesasAgregadasItem); 
                }
              }
            } catch (error) {
              console.error(`Error al procesar la mesa ${img.id}:`, error);
            }
          }
        }
        if(this.idUpdate.length > 0){
          this.actualizarMesas(this.idUpdate);
        }
        if(this.idDelete.length > 0){
          this.eliminarMesas(this.idDelete);
        }
        if(this.idNew.length > 0){
          this.agregarMesa(this.idNew);
        }       
        Swal.fire({
          icon: 'success',
          title: 'Éxito',
          text: 'Mesas actualizadas'
        });   
        window.location.reload();
      }
      
      this.isEditMode = !this.isEditMode;
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
          enabled: this.isEditMode,
        })
    },
    dragMoveListener(event) {
      const target = event.target;

      const draggableElement = target.closest('.draggable-image');
      const id = draggableElement ? draggableElement.dataset.id : null; 

      const x = (parseFloat(draggableElement.getAttribute('data-x')) || 0) + event.dx;
      const y = (parseFloat(draggableElement.getAttribute('data-y')) || 0) + event.dy;

      draggableElement.style.transform = `translate(${x}px, ${y}px)`;
      draggableElement.setAttribute('data-x', x);
      draggableElement.setAttribute('data-y', y);

      const img = this.images.find(image => image.id == id);
      if (img) {
        img.x = x; 
        img.y = y; 

        const mesa = this.mesasAgregadas.find(mesa => mesa.id === img.id);
        if (mesa) {
          mesa.posicion_x = x; 
          mesa.posicion_y = y; 

          console.log(`Mesa ID: ${mesa.id} movida a nueva posición:`, { x: mesa.posicion_x, y: mesa.posicion_y });
        }
      }
    },

    reserve() {
      this.$router.push({ 
        path: '/resevarForm',
        query: { mesa: this.selectedImage.id } 
      });
      console.log("id mesa " + this.selectedImage);
      this.selectedImage = null; 
    },
    
    viewImage() {
      this.$router.push({
        path: '/fotos',
        query: { mesaId: this.selectedImage.id }
      });
    },

    duplicateImage(externalImg) {
      const container = this.$refs.imageContainer;
      const containerRect = container.getBoundingClientRect();
      
      const offset = 20; 
      const newPositionX = containerRect.width / 2 - 82.5; 
      const newPositionY = containerRect.height / 2 - 82.5; 

      let positionX = newPositionX;
      let positionY = newPositionY;

      this.images.forEach(img => {
        if (Math.abs(img.x - newPositionX) < 165 && Math.abs(img.y - newPositionY) < 165) {
          positionX += offset; 
        }
      });

      const newImg = {
        id: this.mesasAgregadas.length + 1,
        name: externalImg.name,
        src: externalImg.src,
        width: 165, 
        height: 165,
        x: positionX,
        y: positionY,
        capacidad: externalImg.capacidad,
        num_mesa: externalImg.num_mesa
      };
      
      // Agregar mesa a la lista mesasAgregadas
      const mesaAgregada = {
        id: this.mesasAgregadas.length + 1,
        capacidad: externalImg.capacidad,
        imagenes: {},
        posicion_x: positionX,
        posicion_y: positionY,
        num_mesa: externalImg.num_mesa
      };

      this.mesasAgregadas.push(mesaAgregada);

      console.log('Mesas Agregadas:', this.mesasAgregadas);
      console.log('Datos de Mesa Agregada:', mesaAgregada);

      this.images.push(newImg);
      
      this.$nextTick(() => {
        const imgElement = this.$refs.imageContainer.querySelector(`.draggable-image[data-id="${newImg.id}"]`);
        if (imgElement) {
          imgElement.style.transform = `translate(${positionX}px, ${positionY}px)`;
          imgElement.setAttribute('data-x', positionX);
          imgElement.setAttribute('data-y', positionY);
        }
      });
    },
    eliminarMesaLista(id) {
      this.images = this.images.filter(img => img.id !== id);
      this.mesasAgregadas = this.mesasAgregadas.filter(mesa => mesa.id !== id);

    },
    async addImagen(id) {
      try {
        const result = await Swal.fire({
          title: "Seleccionar imagen",
          input: "file",
          inputAttributes: {
            "accept": "image/*",
            "aria-label": "Subir imagen"
          }
        });

        if (result.value) {
          const file = result.value;
          const reader = new FileReader();
          
          reader.onload = async (e) => {
            const fileUrl = e.target.result;
            const base64Image = fileUrl.split(',')[1];
            
            const img = this.images.find(image => image.id === id);
            if (img) {
              const imgElement = this.$refs.imageContainer.querySelector(`.draggable-image[data-id="${id}"]`);
              const posX = parseFloat(imgElement.getAttribute('data-x') || 0);
              const posY = parseFloat(imgElement.getAttribute('data-y') || 0);

              const imagenJson = JSON.stringify({
                nombre: file.name,
                base64: base64Image
              });

              const mesaExistente = this.mesasAgregadas.find(mesa => mesa.id === id);

              if (mesaExistente) {
                mesaExistente.imagenes = imagenJson;
              } else {
                const mesaAgregada = {
                  id: id,
                  capacidad: null,
                  imagenes: imagenJson,
                  posicion_x: posX,
                  posicion_y: posY
                };

                this.mesasAgregadas.push(mesaAgregada);
              }

              // Actualizar la imagen en images
              img.uploadedImage = {
                name: file.name,
                base64: base64Image,
                src: fileUrl
              };

              await Swal.fire({
                title: "Imagen subida",
                imageUrl: fileUrl,
                imageAlt: "Imagen subida"
              });
            }
          };

          reader.readAsDataURL(file);
        }
      } catch (error) {
        console.error("Error al cargar la imagen:", error);
      }
    },
    resizeMove(event) {
      if (!this.isEditMode) return; 

      const target = event.target;
      const img = this.images.find(image => image.id == target.dataset.id);

      if (img) {
        img.width += event.deltaRect.width;
        img.height += event.deltaRect.height;

        target.style.width = `${img.width}px`;
        target.style.height = `${img.height}px`;

        const imageElement = target.querySelector('img');
        if (imageElement) {
          imageElement.style.width = `${img.width}px`;
          imageElement.style.height = `${img.height}px`;
        }
      }
    },

    initResize(event, img) {
      if (!event || !img) {
        console.error("El evento o la imagen no están definidos");
        return;
      }
      event.preventDefault();
    },
    async cambiarCapacidad(id) {
      const mesa = this.mesasAgregadas.find(mesa => mesa.id === id);
      if (!mesa) {
        console.error("Mesa not found");
        return;
      }

      const actual = mesa.capacidad;
      const userResponse = await Swal.fire({
        title: 'Gestionar Capacidad',
        text: `La capacidad actual de la mesa es ${actual}. ¿Desea cambiarla?`,
        input: 'text',
        inputPlaceholder: 'Ingrese nueva capacidad',
        showCancelButton: true,
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar',
      });

      if (userResponse.isConfirmed) {
        const CapacidadNueva = userResponse.value;

        if (CapacidadNueva !== '' && !isNaN(CapacidadNueva)) {
          mesa.capacidad = parseInt(CapacidadNueva); 
          console.log(`Capacidad de la mesa ${id} actualizada a: ${mesa.capacidad}`);

          Swal.fire({
            icon: 'success',
            title: 'Capacidad Actualizada',
            text: `La capacidad de la mesa ${id} se ha actualizado a ${mesa.capacidad}.`
          });
        } else {
          console.error("Capacidad no válida");
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Por favor, ingrese una capacidad válida.'
          });
        }
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
  background-image: url('../../assets/images/piso.png');
  background-size: 100px 100px;
  background-repeat: repeat;
  background-position: center;
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

.button-container {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.draggable-image:hover .button-container {
  opacity: 1;
}

.action-button {
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.action-button:hover {
  transform: scale(1.1);
}

.delete-button {
  background-color: #ff5252;
}

.delete-button:hover {
  background-color: #ff1744;
}

.add-image-button {
  background-color: #2196F3;
}

.add-image-button:hover {
  background-color: #1976D2;
}

.manage-capacity-button {
  background-color: #2196F3;
}

.manage-capacity-button:hover {
  background-color: #1976D2;
}

.v-expand-transition-enter-active,
.v-expand-transition-leave-active {
  transition: all 0.3s ease-out;
}

.v-expand-transition-enter-from,
.v-expand-transition-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

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
