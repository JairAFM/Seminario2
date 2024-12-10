<template>
    <v-row no-gutters>
        <v-col
            v-for="(m, index) in mantenimientos"
            :key="index"
            cols="12"
            sm="4"
        >
            <div class="pa-2">
                <cardMaintenance :title="m.title" :descrip="m.descrip" :link="m.link" :icon="m.icon" />
            </div>
        </v-col>
    </v-row>
</template>
<script>
    export default {
        data() {
            return {
                mantenimientos: [
                    {
                        title: 'Categorias',
                        descrip: 'Gestiona eficientemente las categorías para tu menú',
                        link: '/maintenances/categories',
                        icon: 'mdi-shape'
                    },
                    {
                        title: 'menú',
                        descrip: 'Gestiona eficientemente el menú de tu restaurante',
                        link: '/maintenances/menu',
                        icon: 'mdi-silverware'
                    },
                    {
                        title: 'Configuración',
                        descrip: 'Gestiona la información y apariencia de tu restaurante',
                        link: '/maintenances/tables',
                        icon: 'mdi-table-furniture'
                    },
                    {
                        title: 'Puestos',
                        descrip: 'Gestiona eficientemente los puestos de tus empleados',
                        link: '/maintenances/positionEmployee',
                        icon: 'mdi-account-wrench'
                    },
                    {
                        title: 'Empleados',
                        descrip: 'Gestiona eficientemente a tus empleados para obtener un mejor rendimiento',
                        link: '/maintenances/employees',
                        icon: 'mdi-account-group'
                    },
                    {
                        title: 'Estados',
                        descrip: 'Gestiona eficientemente el estados que las ordenes pueden tener',
                        link: '/maintenances/status',
                        icon: 'mdi-list-status'
                    },
                ]
            }
        }
    }
</script>