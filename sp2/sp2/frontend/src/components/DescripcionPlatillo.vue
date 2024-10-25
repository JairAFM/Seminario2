<template>
  <div id="app">
    <h1>Imágenes con Descripcion</h1>

    <!-- Sección para cada imagen precargada -->
    <div v-for="(image, index) in images" :key="index" class="image-upload">
      <!-- Mostrar imagen precargada -->
      <img :src="image.src" alt="Platillo" class="preloaded-image" />

      <!-- Cuadro de texto para descripción -->
      <textarea
        v-model="image.description"
        placeholder="Descripción"
        class="description-input"
      ></textarea>

      <!-- Botón que cambia según el contenido del cuadro de texto -->
      <div class="button-group">
        <button v-if="image.description" @click="saveDescription(index)">Guardar</button>
        <button v-else @click="uploadImage(index)">Generar Descripción</button>
      </div>
      
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: [
        { src: require('@/../src/assets/comida1.png'), description: '', result: '' },
        { src: require('@/../src/assets/comida2.png'), description: '', result: '' },
        { src: require('@/../src/assets/comida3.png'), description: '', result: '' },
      ],
    };
  },
  methods: {
    async uploadImage(index) {
      const image = this.images[index];

      try {
        const response = await fetch(image.src);
        const blob = await response.blob();
        const formData = new FormData();
        formData.append('image', blob, `image${index + 1}.jpg`);

        const analyzeResponse = await fetch('http://localhost:5000/analyze', {
          method: 'POST',
          body: formData,
        });
        const data = await analyzeResponse.json();

        this.images[index].description = data.description;
        this.images[index].result = data.description;
      } catch (error) {
        console.error('Error:', error);
      }
    },

    saveDescription(index) {
      const image = this.images[index];
      image.result = `Descripción guardada: ${image.description}`;
      console.log(`Descripción de la imagen ${index + 1}: ${image.description}`);
    },
  },
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  margin: 50px;
  text-align: center;
}
.image-upload {
  margin-bottom: 30px;
  border: 1px solid #ddd; /* Agregar un borde alrededor de cada imagen */
  padding: 20px; /* Espaciado interno */
  border-radius: 8px; /* Bordes redondeados */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Sombra suave */
  background-color: #f9f9f9; /* Color de fondo ligero */
}
.preloaded-image {
  width: 100px;
  height: auto;
  margin-bottom: 10px;
}
.description-input {
  margin: 10px 0;
  padding: 10px; /* Mayor padding para un mejor aspecto */
  width: calc(100% - 22px); /* Ajustar el ancho para incluir el padding */
  height: 60px; /* Altura fija para el área de texto */
  border: 1px solid #ccc; /* Borde claro */
  border-radius: 4px; /* Bordes redondeados */
  font-size: 14px; /* Tamaño de fuente más legible */
  resize: none; /* Deshabilitar el redimensionamiento */
}
.button-group {
  margin: 10px 0;
}
.button-group button {
  margin-right: 5px; /* Espaciado entre botones */
  padding: 8px 12px; /* Padding para botones */
  font-size: 14px; /* Tamaño de fuente para botones */
  border: none; /* Sin borde */
  border-radius: 4px; /* Bordes redondeados */
  cursor: pointer; /* Cambiar cursor al pasar sobre el botón */
  background-color: #007bff; /* Color de fondo azul */
  color: white; /* Color de texto blanco */
  transition: background-color 0.3s; /* Efecto de transición para el color */
}
.button-group button:hover {
  background-color: #0056b3; /* Color más oscuro al pasar el ratón */
}
.result {
  margin-top: 10px;
  font-size: 16px;
  color: green;
  font-weight: bold; /* Negrita para el resultado */
}
</style>
