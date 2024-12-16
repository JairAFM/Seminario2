<template>
  <div class="reservation-container mt-5">
    <h1 class="mb-4 text-center text-primary">Formulario de Reservación</h1>
    <form @submit.prevent="submitForm" class="reservation-form">
      <div class="mb-3">
        <label for="date" class="form-label">Fecha:</label>
        <input 
          type="date" 
          id="date" 
          v-model="reservation.date" 
          class="form-control custom-input" 
          :min="minDate"
          required 
        />
      </div>
      <div class="mb-3">
        <label for="start-time" class="form-label">Hora de Inicio:</label>
        <input 
          type="time" 
          id="start-time" 
          v-model="reservation.startTime" 
          class="form-control custom-input" 
          :min="minTime"
          :max="maxTime"
          :disabled="isTimeDisabled"
          @change="validateTimeOnChange"
          required 
        />
        <small v-if="isTimeDisabled" class="text-danger">
          Por favor seleccione una hora válida posterior a la actual
        </small>
      </div>
  
      <div class="mb-3">
        <label for="guests" class="form-label">Número de Personas:</label>
        <select id="guests" v-model="guestCount" class="form-select custom-select">
          <option value="" disabled selected>Elegir cantidad</option>
          <option v-for="n in mesaCapacidad" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>

      <button type="submit" class="btn btn-submit">Reservar</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'ReservationForm',
  data() {
    return {
      reservation: {
        date: '',
        startTime: '', 
        customGuests: null,
        mesa: null, 
      },
      cantidad_sillas: 0,
      ahora: new Date(),
      dia: "",
      hora: "",
      minDate: '',
      minTime: '00:00',
      maxTime: '23:59',
      isTimeDisabled: false,
      mesaCapacidad: '',
      guestCount: '',
      userId: null,
      mesaId: 0, 
      ordenId: null,
      tipoUser: null,
      capacidad_t: 0
    };
  },
  async created() {
    // Obtener el ID de la mesa de la URL
    this.mesaId = window.location.href.split("?")[1].split("=")[1];
    this.userId = localStorage.getItem('userId');
    this.tipoUser = localStorage.getItem('tipoUser');
    
    try {
      const response = await fetch(`http://127.0.0.1:5000/obtenerMesa/${this.mesaId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const mesaData = await response.json();
      console.log('Capacidad de la mesa:', mesaData.capacidad);
      
      this.mesaCapacidad = mesaData.capacidad;
    } catch (error) {
      console.error('Error al obtener datos de la mesa:', error);
    }
  },
  mounted() {
    const mesa = this.$route.query.mesa; 
    this.reservation.mesa = mesa; 
    this.dia = this.ahora.getDate() + " " + this.ahora.getMonth() + " " + this.ahora.getFullYear();
    this.hora = this.ahora.getHours();

    this.setSillaCount(mesa);
    this.setMinDateTime();

    this.fetchMesaData(mesa).then(mesaData => {
      this.mesaCapacidad = mesaData.capacidad;
      this.guestCount = this.mesaCapacidad;
    });
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
          this.cantidad_sillas = 0; 
          break;
      }
    },
    setMinDateTime() {
      const today = new Date();
      this.minDate = today.toISOString().split('T')[0];
      this.updateMinTime();
    },
    updateMinTime() {
      const today = new Date();
      const selectedDate = new Date(this.reservation.date + 'T00:00:00');
      
      const isSameDay = selectedDate.getDate() === today.getDate() &&
                        selectedDate.getMonth() === today.getMonth() &&
                        selectedDate.getFullYear() === today.getFullYear();
      
      if (isSameDay) {
        const hours = String(today.getHours()).padStart(2, '0');
        const minutes = String(today.getMinutes()).padStart(2, '0');
        this.minTime = `${hours}:${minutes}`;
        this.maxTime = '23:59';
        this.isTimeDisabled = false;

        if (this.reservation.startTime && this.reservation.startTime < this.minTime) {
          this.reservation.startTime = '';
          this.isTimeDisabled = true;
        }
      } else {
        this.minTime = '00:00';
        this.maxTime = '23:59';
        this.isTimeDisabled = false;
      }
    },
    validateTimeOnChange(event) {
      const today = new Date();
      const selectedDate = new Date(this.reservation.date + 'T00:00:00');
      const selectedTime = event.target.value;
      
      const isSameDay = selectedDate.getDate() === today.getDate() &&
                        selectedDate.getMonth() === today.getMonth() &&
                        selectedDate.getFullYear() === today.getFullYear();
      
      if (isSameDay) {
        const currentHour = String(today.getHours()).padStart(2, '0');
        const currentMinutes = String(today.getMinutes()).padStart(2, '0');
        const currentTime = `${currentHour}:${currentMinutes}`;
        
        if (selectedTime < currentTime) {
          event.preventDefault();
          this.reservation.startTime = '';
          this.isTimeDisabled = true;
          setTimeout(() => {
            this.isTimeDisabled = false;
          }, 1500);
        }
      }
    },
    submitForm() {
      if (!this.guestCount) {
        this.guestCount = this.mesaCapacidad;
      }

      const datetime = new Date(`${this.reservation.date}T${this.reservation.startTime}`);

      const dataToSend = {
        id_mesa: this.mesaId,
        id_cliente: this.userId,
        id_orden: this.ordenId,
        inicio: `${this.reservation.date}T00:00:00`, 
        hora: this.reservation.startTime, 
        no_personas: this.guestCount,
        id_estado: 1
      };

      console.log("Formulario enviado con los datos:", dataToSend);

      axios.post('http://localhost:5000/reservaciones', dataToSend)
        .then(response => {
          Swal.fire({
            icon: 'success',
            title: 'Éxito',
            text: 'Reserva creada con éxito'
          });  
          console.log("Reserva creada con éxito:", response.data);
        })
        .catch(error => {
          console.error("Error al crear la reserva:", error.response.data);
        });
    },
    async fetchMesaData(mesaId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/obtenerMesa/${mesaId}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
      } catch (error) {
        console.error('Error fetching mesa data:', error);
      }
    },
  },
  watch: {
    'reservation.date'() {
      this.updateMinTime();
    }
  }
};
</script>

<style scoped>
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

input:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
}

.text-danger {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}
</style>
