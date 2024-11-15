<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <slot></slot>
        <button @click="$emit('close')">Cerrar</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CustomModal',
  };
  </script>
  