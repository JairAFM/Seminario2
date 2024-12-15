<template>
      <div class="card-wrap">
        <!-- Icono dinámico -->
        <div class="card-header">
          <v-icon :icon="icon" size="5rem" class="fas fa-code"></v-icon>
        </div>
        <!-- Título -->
        <div class="card-content">
          <h1 class="card-title">{{ title }}</h1>
          <!-- Descripción -->
          <p class="card-text">{{ descrip }}</p>
          <v-card-actions class="d-flex justify-end">
            <!-- Botón con enlace dinámico -->
              <div class="card-btn">
                <v-btn :to="link">
                  Ir
                  <v-icon icon="mdi-location-enter"></v-icon>
                </v-btn>
              </div>
          </v-card-actions>
        </div>
      </div>
</template>

<script>
export default {
  props: {
    title: String,
    descrip: String,
    link: String,
    icon: String
  }
}
</script>

<style scoped>
*{
  margin:0px;
  padding:0px;
  box-sizing: border-box;
}
:root{
  --color-text: #616161;
  --color-text-btn: #ffffff;
}
body{
  font-family: 'Roboto', sans-serif;
  background: linear-gradient(to right, #8e9eab, #eef2f3); 
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 30px;
}
.card-wrap{
  width: 220px;
  background: #fff;
  border-radius: 20px;
  border: 5px solid #fff;
  overflow: hidden;
  color: var(--color-text);
  box-shadow: rgba(0, 0, 0, 0.19) 0px 10px 20px,
              rgba(0, 0, 0, 0.23) 0px 6px 6px;
  cursor: pointer;
  transition: all .2s ease-in-out;
}
.card-wrap:hover{
  transform: scale(1.1);
}
.card-header{
  height: 200px;
  width: 100%;
  background: #77f454;
  border-radius:100% 0% 100% 0% / 0% 50% 50% 100%;
  display: grid;
  place-items: center;

}

.card-header i{
  color: #fff;
  font-size: 72px;
}
.card-content{
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 60%;
  margin: 0 auto;
}
.card-title{
  text-align: center;
  text-transform: uppercase;
  font-size: 16px;
  margin-top: 10px;
  margin-bottom: 20px;
  
}
.card-text{
  text-align: center;
  font-size: 12px;
  margin-bottom: 20px;
}
.card-btn{
  border: none;
  border-radius: 100px;
  padding: 5px 30px;
  color: #0de916;
  margin-bottom: 15px;
  text-transform: uppercase;
}
.card-header.one{
  background: linear-gradient(to bottom left, var(--card1-gradient-color1), var(--card1-gradient-color2));
}
.card-header.two{
  background: linear-gradient(to bottom left, var(--card2-gradient-color1), var(--card2-gradient-color2));
}
.card-header.three{
  background: linear-gradient(to bottom left, var(--card3-gradient-color1), var(--card3-gradient-color2));
}
.card-header.four{
  background: linear-gradient(to bottom left, var(--card4-gradient-color1), var(--card4-gradient-color2));
}

.card-btn.one{
  background: linear-gradient(to left, var(--card1-gradient-color1), var(--card1-gradient-color2));
}
.card-btn.two{
  background: linear-gradient(to left, var(--card2-gradient-color1), var(--card2-gradient-color2));
}
.card-btn.three{
  background: linear-gradient(to left, var(--card3-gradient-color1), var(--card3-gradient-color2));
}
.card-btn.four{
  background: linear-gradient(to left, var(--card4-gradient-color1), var(--card4-gradient-color2));
}
</style>
