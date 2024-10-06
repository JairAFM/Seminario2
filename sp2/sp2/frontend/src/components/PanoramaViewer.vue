<template>
    <div id="panorama-container" style="width: 100%; height: 500px;"></div>
  </template>
  
  <script>
  import * as PANOLENS from 'panolens';
  
  export default {
    mounted() {
      const panoramaContainer = document.getElementById('panorama-container');
  
      // Crear un panorama con la imagen de tu servidor Flask
      const panorama = new PANOLENS.ImagePanorama('http://localhost:5000/static/img/foto4.jpeg');
      const viewer = new PANOLENS.Viewer({ container: panoramaContainer });
  
      viewer.add(panorama);
    }
  };
  </script>
  
  <style scoped>
  /* Añade estilos si es necesario */
  </style>
  