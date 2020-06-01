<template>
  <v-container fluid class="py-0 justify-start align-stretch fill-height d-flex">
    <v-row class="h-100" justify="start" align="stretch">
      <v-card tile class="col-md-4 px-0 d-flex flex-column py-0">
        <v-toolbar class="w-100 flex-grow-0" tile dense>
          <v-toolbar-title>Categorias</v-toolbar-title>

          <v-spacer></v-spacer>

          <v-btn icon>
            <v-icon>mdi-plus</v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon>mdi-magnify</v-icon>
          </v-btn>
        </v-toolbar>
        <v-list class="flex-grow-1 h-100">
          <template v-for="(item) in categories">
            <v-list-item :to='`/management/cat/${item.pk}/`' :key="item.pk">
              <v-list-item-content>
                <v-list-item-title v-html="item.name"></v-list-item-title>
                <v-list-item-subtitle v-html="`Quantidade disponível: ${item.amount}`"></v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list>
      </v-card>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import app from "@/sdk";
import { Category } from "../models";
export default Vue.extend({
  name: "management",
  data: () => ({
    categories: null,
  }),
  beforeMount(){
    Category.api().get('categories').then(({ response }) => {
      this.categories = response.data
    })
  }
});
</script>
