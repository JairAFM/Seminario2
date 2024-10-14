<template>
    <v-app-bar
        color="amber-lighten-3"
      >
        <v-app-bar-title>
            <v-btn variant="plain" to="/">
                <template v-slot:prepend>            
                    <v-img
                    :width="50"
                    aspect-ratio="4/3"
                    cover
                    src="../../assets/images/findTable.png"
                    rounded="circle"
                    ></v-img>
                </template> 
                findTable
            </v-btn>
        </v-app-bar-title>
        <v-spacer></v-spacer>        
        
        <v-row>
            <v-col cols="12" class="d-flex justify-end px-6">
                <div class="text-center">
                    <v-menu
                        v-model="menu"
                        :close-on-content-click="false"
                        location="bottom"
                    >
                        <template v-slot:activator="{ props }">
                            <v-btn 
                                size="small" 
                                variant="flat" 
                                color="light-blue-lighten-3" 
                                append-icon="mdi-login" 
                                @click="menu = !menu"
                            >
                                Inicia Sesión
                            </v-btn>
                        </template>
                        <v-card 
                                class="mx-auto"
                                min-width="300"
                            >
                            <v-card-title 
                                style="background-color: #ffe082;"
                                class="mb-2 text-center"
                            >
                                Inicia Sesión
                            </v-card-title>
                            <v-list class="pa-1">
                                <v-form
                                    v-model="form"
                                    @submit.prevent="singIn"
                                >
                                    <v-text-field
                                        class="mb-2"
                                        v-model="email"
                                        :rules="emailRules"
                                        label="Correo Electrónico"
                                        variant="outlined"
                                        required
                                        clearable
                                    ></v-text-field>
                                    <v-text-field
                                        class="mb-2"
                                        v-model="password"
                                        :readonly="loading"
                                        :rules="passRules"
                                        :type="showPassword ? 'text' : 'password'"
                                        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                        @click:append="showPassword = !showPassword"
                                        label="Contraseña"
                                        variant="outlined"
                                        clearable
                                        required
                                    ></v-text-field>
                                    <v-btn
                                        :loading="loading"
                                        color="green-lighten-1"
                                        size="large"
                                        type="submit"
                                        variant="elevated"
                                        block
                                    >
                                        Iniciar Sesión
                                    </v-btn>
                                    <hr class="my-2"/>
                                    <p class="my-2 text-center" style="color:#424EFC;">
                                        ¿No tienes una cuenta?
                                    </p>
                                    <v-btn
                                        size="large"
                                        variant="elevated"
                                        color="light-blue-lighten-3"
                                        block
                                        to="/crearCuenta"
                                    >
                                        Crear Cuenta
                                    </v-btn>
                                </v-form>
                            </v-list>
                        </v-card>
                    </v-menu>
                </div>
            </v-col>
        </v-row>
    </v-app-bar>
</template>
<script>
    export default {
        data: () => ({
            menu: false,
            form: false,
            email: '',
            emailRules: [
                value => {
                    if (value) return true
                    return 'El correo electrónico es requerido.'
                },
                value => {
                    if (/.+@.+\..+/.test(value)) return true
                    return 'El correo electrónico es inválido.'
                },
            ],
            password: null,
            passRules: [
                value => {
                    if (value) return true
                    return 'La contraseña es requerida.'
                },
            ],
            loading: false,
            showPassword: false,
        }),
        methods: {
            singIn () {
                if (!this.form) return

                this.loading = true

                setTimeout(() => (this.loading = false), 2000)
            },
        },
    }
</script>