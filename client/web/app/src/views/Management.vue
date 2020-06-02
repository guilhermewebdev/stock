<template>
  <v-container fluid v-resize="resize" :style="`height: ${height}px;`" class="py-0">
    <v-row class="h-100" justify="start" align="stretch" :style="`height: ${height}px;`">
      <v-card
        tile
        class="col-md-3 h-100 px-0 d-flex position-relative flex-column py-0"
        :style="`height: ${height}px;`"
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
                  :rotate="270"
                  :value="(item.amount/item.minimum)*50"
                  :color="item.amount === 0 ?
                   'error' : item.amount < item.minimum ?
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
      <v-col md="9">
        <v-expansion-panels focusable v-if="$route.params.pk" hover tile>
          <v-expansion-panel>
            <v-expansion-panel-header>{{ selected.name }}</v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-progress-linear
                :color="selected.amount === 0 ?
                   'error' : selected.amount < selected.minimum ?
                    'warning' : 'success'"
                :value="(selected.amount/selected.minimum)*50"
              ></v-progress-linear>
              
              <v-row justify="space-between" dense>
                <v-col cols="3">
                  <span>Quantidade Disponível:</span>
                  <span>{{ selected.amount }}</span>
                </v-col>
                <v-col cols="3">
                  <span>Quantidade Mínima:</span>
                  <span>{{ selected.minimum }}</span>
                </v-col>
                <v-col cols="3">
                  <span>Data de Cadastro:</span>
                  <span>{{ new Date(selected.registration).toLocaleString('pt-BR', { timeZone: 'UTC' }) }}</span>
                </v-col>
              </v-row>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        
      </v-col>
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
    categories: null,
    height: window.innerHeight - 48
  }),
  beforeMount() {
    this.refresh();
  },
  computed: {
    selected() {
      return this.categories.filter(
        item => item.pk == this.$route.params.pk
      )[0];
    }
  },
  methods: {
    refresh() {
      Category.api()
        .get("categories")
        .then(({ response }) => {
          this.categories = response.data;
        });
    },
    resize() {
      this.height = window.innerHeight - 60;
    }
  },
  components: {
    CreateCategory
  }
});
</script>
