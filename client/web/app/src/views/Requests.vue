<template>
  <v-container fluid class="h-100 overflow-y-auto">
    <v-data-iterator
      :items="requests"
      :items-per-page.sync="itemsPerPage"
      :page="page"
      :search="search"
      :sort-by="sortBy"
      :sort-desc="sortDesc"
      class="elevation-0 px-3"
    >
      <template v-slot:header>
        <v-toolbar color="light" elevation="0" class="mb-1">
          <v-text-field
            v-model="search"
            clearable
            solo
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Buscar"
          ></v-text-field>
          <template v-if="$vuetify.breakpoint.mdAndUp">
            <v-spacer></v-spacer>
            <v-select
              v-model="sortBy"
              solo-inverted
              hide-details
              :items="keys"
              prepend-inner-icon="mdi-sort"
              label="Ordenar por"
            ></v-select>
            <v-spacer></v-spacer>
            <v-btn-toggle v-model="sortDesc" mandatory>
              <v-btn large depressed color="light" :value="false">
                <v-icon>mdi-arrow-up</v-icon>
              </v-btn>
              <v-btn large depressed color="light" :value="true">
                <v-icon>mdi-arrow-down</v-icon>
              </v-btn>
            </v-btn-toggle>
          </template>
        </v-toolbar>
      </template>
      <template v-slot:default="props">
        <v-row>
          <v-col v-for="item in props.items" :key="item.name" cols="12" sm="6" md="5" lg="4">
            <v-card outlined tile>
              <v-card-title
                class="subheading font-weight-bold"
              >{{ consumers[item.consumer_type] }} {{ item.consumer }}</v-card-title>
              <v-card-subtitle>
                {{ new Date(item.registration).toLocaleString("pt-BR", {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric"
                }) }}
              </v-card-subtitle>
              <v-divider></v-divider>
              <v-card-text v-if="item.note">Observações: {{ item.note }}</v-card-text>
              <v-list>
                <v-list-item link v-for="(product) in item.products" :key="product.pk">
                  <v-list-item-content
                    :class="{ 'blue--text': sortBy === key }"
                  >{{ product.product.name }}: {{ product.amount }}</v-list-item-content>
                  <v-list-item-content class="align-end">Disponível: {{ product.product.amount }}</v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
  </v-container>
</template>
<script lang="ts">
import Vue from "vue";
import connect from "../connect";
export default Vue.extend({
  name: "requests",
  data: () => ({
    requests: [],
    itemsPerPageArray: [4, 8, 12],
    search: "",
    filter: {},
    sortDesc: false,
    page: 1,
    itemsPerPage: 4,
    sortBy: "consumer",
    keys: [
      { text: "Tipo de consumidor", value: "consumer_type" },
      { text: "Consumidor", value: "consumer" },
      { text: "Data da requisição", value: "registration" }
    ],
    consumers: {
      user: "Usuário",
      dentist: "Dentista",
      chamber: "Consultório",
      patient: "Paciente",
      other: "Outro"
    }
  }),
  computed: {
    numberOfPages() {
      return Math.ceil(this.items.length / this.itemsPerPage);
    },
    filteredKeys() {
      return this.keys;
    }
  },
  beforeMount() {
    this.refresh();
  },
  methods: {
    async refresh() {
      connect
        .get("requests/consum/?format=json")
        .then(({ data }) => (this.requests = data));
    },
    nextPage() {
      if (this.page + 1 <= this.numberOfPages) this.page += 1;
    },
    formerPage() {
      if (this.page - 1 >= 1) this.page -= 1;
    },
    updateItemsPerPage(number) {
      this.itemsPerPage = number;
    }
  }
});
</script>