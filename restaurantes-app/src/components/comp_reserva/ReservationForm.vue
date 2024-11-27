<template>
    <div class="reservation-container mt-5">
      <h1 class="mb-4 text-center text-primary">Formulario de Reservación</h1>
      <form @submit.prevent="submitForm" class="reservation-form">
        <div class="mb-3">
          <label for="date" class="form-label">Fecha:</label>
          <input type="date" id="date" v-model="reservation.date" class="form-control custom-input" required />
        </div>
  
        <!-- Campo de Hora de Inicio -->
        <div class="mb-3">
          <label for="start-time" class="form-label">Hora de Inicio:</label>
          <input type="time" id="start-time" v-model="reservation.startTime" class="form-control custom-input" required />
        </div>
  
        <!-- Campo de Hora Final -->
        <div class="mb-3">
          <label for="end-time" class="form-label">Hora Final:</label>
          <input type="time" id="end-time" v-model="reservation.endTime" class="form-control custom-input" required />
        </div>
  
        <div class="mb-3">
          <label for="guests" class="form-label">Número de Personas:</label>
          <select id="guests" v-model="guestCount" class="form-select custom-select" required>
            <option value="" disabled selected>Elegir cantidad</option>
            <option :value="cantidad_sillas">Número de sillas de la mesa seleccionada ({{ cantidad_sillas }})</option>
            <option value="personalizado">Elegir cantidad personalizada</option>
          </select>
        </div>
  
        <!-- Mostrar el input solo si la opción es 'personalizado' -->
        <div v-if="guestCount === 'personalizado'" class="mb-3">
          <label for="customGuests" class="form-label">Cantidad:</label>
          <input type="number" id="customGuests" v-model="reservation.customGuests" class="form-control custom-input" required min="1" />
        </div>
  
        <button type="submit" class="btn btn-submit">Reservar</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ReservationForm',
    data() {
      return {
        guestCount: '', // Para almacenar la opción seleccionada
        reservation: { // Para almacenar los datos de la reserva
          date: '',
          startTime: '', // Hora de inicio
          endTime: '', // Hora final
          customGuests: null,
          mesa: null, // Añadir la propiedad para el número de mesa
        },
        cantidad_sillas: 0, // Variable para almacenar la cantidad de sillas
      };
    },
    mounted() {
      const mesa = this.$route.query.mesa; // Obtener el número de mesa de los parámetros de consulta
      this.reservation.mesa = mesa; // Guardar el número de mesa en el objeto de reserva
      console.log('Número de mesa:', mesa);
  
      // Establecer la cantidad de sillas según el id de la mesa
      this.setSillaCount(mesa);
    },
    methods: {
      setSillaCount(mesaId) {
        switch (mesaId) {
          case '1':
            this.cantidad_sillas = 3;
            break;
          case '2':
            this.cantidad_sillas = 4;
            break;
          case '3':
            this.cantidad_sillas = 6;
            break;
          case '4':
            this.cantidad_sillas = 8;
            break;
          default:
            this.cantidad_sillas = 0; // O puedes asignar un valor por defecto
            break;
        }
      },
      submitForm() {
        // Definir el número de personas
        const numberOfGuests = this.guestCount === 'personalizado' ? this.reservation.customGuests : this.cantidad_sillas;
  
        // Preparar los datos a enviar, asegurando que el número de mesa sea un entero
        const dataToSend = {
          id_usuario: 1, // Cambia esto por el ID real del usuario
          id_estado: 1,  // Cambia esto por el ID real del estado de la reserva
          fecha_reserva: this.reservation.date,
          hora_inicio: this.reservation.startTime, // Hora de inicio
          hora_final: this.reservation.endTime, // Hora final
          cantidad_personas: numberOfGuests,
          mesa: parseInt(this.reservation.mesa, 10), // Convertir el número de mesa a entero
        };
  
        // Lógica para enviar el formulario
        console.log("Formulario enviado con los datos:", dataToSend);
  
        // Realizar la solicitud POST
        axios.post('http://localhost:5000/reservas', dataToSend)
          .then(response => {
            console.log("Reserva creada con éxito:", response.data);
          })
          .catch(error => {
            console.error("Error al crear la reserva:", error.response.data);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Contenedor principal */
  .reservation-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    font-size: 2rem;
    color: #4A90E2;
    font-weight: bold;
    text-align: center;
  }
  
  .reservation-form {
    display: flex;
    flex-direction: column;
  }
  
  .form-label {
    font-size: 1.1rem;
    color: #333;
  }
  
  .custom-input,
  .custom-select {
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 12px;
    font-size: 1rem;
    margin-top: 8px;
    transition: all 0.3s ease;
  }
  
  .custom-input:focus,
  .custom-select:focus {
    border-color: #4A90E2;
    outline: none;
    box-shadow: 0 0 5px rgba(74, 144, 226, 0.5);
  }
  
  .btn-submit {
    background-color: #4A90E2;
    color: #fff;
    font-size: 1.1rem;
    padding: 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 20px;
    transition: background-color 0.3s ease;
  }
  
  .btn-submit:hover {
    background-color: #357ABD;
  }
  
  @media (max-width: 600px) {
    .reservation-container {
      padding: 15px;
    }
  
    h1 {
      font-size: 1.5rem;
    }
  
    .custom-input,
    .custom-select {
      padding: 10px;
    }
  
    .btn-submit {
      font-size: 1rem;
    }
  }
  </style>
  