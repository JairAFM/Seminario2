<template>
    <div id="panorama-container" style="width: 100%; height: 500px;"></div>
  </template>
  
  <script>
  import * as PANOLENS from 'panolens';
  
  export default {
    data() {
      return {
        viewer: null,
        vistasMap: {
          1: 'src/assets/images/restaurante_prot.jpg',
          2: 'src/assets/images/vistas/foto5.jpeg',
          3: 'src/assets/images/vistas/foto3.jpeg',
          4: 'src/assets/images/vistas/foto4.jpeg',
          // Añade más mapeos según necesites
        }
      }
    },
    methods: {
      createPanorama(mesaId) {
        const panoramaContainer = document.getElementById('panorama-container');
        const imagePath = this.vistasMap[mesaId] || 'src/assets/images/vistas/foto4.jpeg';
        
        // Si existe un viewer anterior, lo destruimos
        if (this.viewer) {
          this.viewer.dispose();
          this.viewer = null;
        }
        
        const panorama = new PANOLENS.ImagePanorama(imagePath);
        this.viewer = new PANOLENS.Viewer({ container: panoramaContainer });
        this.viewer.add(panorama);
      }
    },
    mounted() {
      const mesaId = this.$route.query.mesaId;
      this.createPanorama(mesaId);
    },
    watch: {
      '$route.query.mesaId': {
        handler(newMesaId) {
          if (newMesaId) {
            this.createPanorama(newMesaId);
          }
        }
      }
    },
    beforeDestroy() {
      // Limpiamos el viewer cuando el componente se destruye
      if (this.viewer) {
        this.viewer.dispose();
        this.viewer = null;
      }
    }
  };
  </script>
  
  <style scoped>
  /* Añade estilos si es necesario */
  </style>
  
