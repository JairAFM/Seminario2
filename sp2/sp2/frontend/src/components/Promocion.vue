<template>
  <div class="promotions-container">
    <h2>Promociones</h2>
    <form @submit.prevent="addPromotion">
      <input
        type="text"
        v-model="newPromotion.title"
        placeholder="Título de la promoción"
        required
      />
      <textarea
        v-model="newPromotion.description"
        placeholder="Descripción de la promoción"
        required
      ></textarea>
      <input
        type="text"
        v-model="newPromotion.discount"
        placeholder="Descuento (%)"
        required
      />
      <button type="submit">Agregar Promoción</button>
    </form>
    <div class="promotion-list">
      <div class="promotion-card" v-for="(promotion, index) in promotions" :key="index">
        <h3>{{ promotion.title }}</h3>
        <p>{{ promotion.description }}</p>
        <p><strong>Descuento: {{ promotion.discount }}%</strong></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newPromotion: {
        title: '',
        description: '',
        discount: ''
      },
      promotions: []
    };
  },
  methods: {
    addPromotion() {
      if (this.newPromotion.title && this.newPromotion.description && this.newPromotion.discount) {
        this.promotions.push({ ...this.newPromotion });
        this.newPromotion.title = '';
        this.newPromotion.description = '';
        this.newPromotion.discount = '';
      }
    }
  }
};
</script>

<style scoped>
.promotions-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

form {
  display: flex;
  flex-direction: column;
}

input,
textarea {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}

.promotion-list {
  margin-top: 20px;
}

.promotion-card {
  border: 1px solid #007bff;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.promotion-card h3 {
  margin: 0;
}
</style>
