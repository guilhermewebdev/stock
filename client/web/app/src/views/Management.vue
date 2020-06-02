<template>
  <v-container fluid class="py-0 h-100">
    <v-row class="h-100" justify="start" align="stretch">
      <v-card
        tile
        class="col-md-3 h-100 px-0 d-flex position-relative flex-column py-0"
        style="overflow: auto;"
      >
        <v-toolbar class="w-100 flex-grow-0" tile dense>
          <v-toolbar-title>Categorias</v-toolbar-title>

          <v-spacer></v-spacer>

          <CreateCategory v-on:created="refresh" />
          <v-btn icon>
            <v-icon>mdi-magnify</v-icon>
          </v-btn>
        </v-toolbar>
        <v-list class="flex-grow-1" style="overflow: auto;">
          <template v-for="(item) in categories">
            <v-list-item :to="`/management/cat/${item.pk}/`" :key="item.pk">
              <v-list-item-avatar>
                <v-progress-circular
                  :size="40"
                  :value="(item.amount/item.minimum)*100"
                  :color="(item.amount/item.minimum)*100 === 0 ?
                   'error' : (item.amount/item.minimum)*100 < 20 ?
                    'warning' : 'success'"
                >{{ item.reference }}</v-progress-circular>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-html="item.name"></v-list-item-title>
                <v-list-item-subtitle>
                  <span>
                    <span>Disponível: {{item.amount}}</span>
                    <span class="ml-5">Mínimo: {{item.minimum}}</span>
                  </span>
                  <v-spacer />
                </v-list-item-subtitle>
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
import CreateCategory from "./CreateCategory";

export default Vue.extend({
  name: "management",
  data: () => ({
    categories: null
  }),
  beforeMount() {
    this.refresh();
  },
  methods: {
    refresh() {
      Category.api()
        .get("categories")
        .then(({ response }) => {
          this.categories = response.data;
        });
    }
  },
  components: {
    CreateCategory
  }
});
</script>
