<template>
    <v-data-table
          :headers="headers"
          :items="categories"
          item-value="id"
          class="elevation-1"
          items-per-page-text="Registros por página"
          :items-per-page-options="[{value: 10, title: '10'},
                                    {value: 20, title: '20'},
                                    {value: 30, title: '30'}]"
        >
          <template v-slot:[`item.actions`]="{ item }">
            <v-btn icon @click="openDialog('edit', item)" class="mx-2">
              <v-icon color="green">mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon @click="deleteCategory(item.id)" class="mx-2">
              <v-icon color="red">mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>   
</template>
<script>
    export default {
        props: {
            headers: Array,
            items: Array,
            
        }
    }
</script>