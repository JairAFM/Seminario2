<template>
  <div id="app">
    <h1>Sube una Imagen de un Platillo</h1>
    <input type="file" ref="imageInput" accept="image/*">
    <button @click="uploadImage">Subir y Analizar</button>
    <div id="result">{{ result }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      result: '',
    };
  },
  methods: {
    async uploadImage() {
      const file = this.$refs.imageInput.files[0];
      
      if (file) {
        const formData = new FormData();
        formData.append('image', file);

        try {
          const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            body: formData,
          });
          const data = await response.json();
          this.result = data.description;
        } catch (error) {
          console.error('Error:', error);
        }
      } else {
        alert("Por favor, selecciona una imagen primero.");
      }
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
#result {
  margin-top: 20px;
  font-size: 18px;
  color: green;
}
</style>
