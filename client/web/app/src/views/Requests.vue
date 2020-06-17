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
              solo
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
        <v-row dense>
          <v-col v-for="item in props.items" :key="item.pk" cols="12" sm="6" md="5" lg="4">
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
              <v-card-actions class="align-end">
                <v-btn color="primary" @click="selected = item; deliveryDialog = true;">Entregar</v-btn>
                <v-spacer />
                <v-dialog v-model="deleteDialog" persistent max-width="290">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn icon v-bind="attrs" v-on="on" @click="selected = item">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title class="headline">Recusar Requisição</v-card-title>
                    <v-card-text>Tem certeza que deseja recusar a requisição?</v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="primary" text @click="deleteDialog = false">Cancelar</v-btn>
                      <v-btn
                        color="primary"
                        text
                        :key="item.pk"
                        @click="recuse(); deleteDialog = false; selected = {};"
                      >Recusar</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
    <v-dialog v-model="deliveryDialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Entregar requisição</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row v-for="(product) in selected.products" :key="product.pk">
              <v-col cols="8" sm="8">
                <v-autocomplete
                  :items="product.product.products.map(item => ({
                                value: item.pk,
                                text: `${item.brand} - ${item.bar_code}`,
                                disabled: item.amount === 0,
                              }))"
                  :label="`${ product.amount }× ${ product.product.name }`"
                ></v-autocomplete>
              </v-col>
              <v-col cols="4">
                <v-text-field min="0" :value="product.amount" type="number" label="Quantidade" />
              </v-col>
            </v-row>
          </v-container>
          <small>* Campos obrigatórios</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="deliveryDialog = false">Fechar</v-btn>
          <v-btn color="primary" text @click="deliveryDialog = false">Entregar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
    selected: {},
    sortDesc: false,
    page: 1,
    deliveryDialog: false,
    deleteDialog: false,
    product_deliveries: [],
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
    numberOfPages: () => Math.ceil(this.items.length / this.itemsPerPage),
    form: () => ({
      request: this.$data.selected.pk
    })
  },
  beforeMount() {
    this.refresh();
  },
  methods: {
    async refresh() {
      connect
        .get("/requests/consum/?format=json")
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
    },
    async recuse() {
      connect
        .delete(`/requests/consum/${this.selected.pk}/`)
        .then(this.refresh);
    },
    async delivery() {
      connect.post("/deliveries/");
    }
  }
});
</script>