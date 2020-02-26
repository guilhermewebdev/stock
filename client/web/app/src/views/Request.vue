<template>
    <v-container>
        <v-row>
            <v-card
                tile
                right
                class="
                    col-12
                    col-xs-10
                    col-sm-8
                    col-md-7
                    col-lg-5
                    col-xg-4
                    mx-auto
                "
            >
                <v-list-item two-line>
                <v-list-item-content>
                    <v-list-item-title class="headline mb-1">Solicitar produto</v-list-item-title>
                    <v-list-item-subtitle>Preencha o formulário com as informações dos produtos que deseja</v-list-item-subtitle>
                </v-list-item-content>
                </v-list-item>
                <v-form
                    ref="form"
                >
                    <v-container>
                        <v-row v-for="product in productsForms" :key="product">
                            <v-col cols="6">
                                <v-autocomplete
                                    label="Produto"
                                    required
                                    autofocus
                                    @click:append-outer="productsForms.splice(product, 1); ajustForms()"
                                    :append-outer-icon="((product > 0) && (product == productsForms[productsForms.length-1]))?'mdi-close':''"
                                    v-model="request.products[product]"
                                    :loading="loadingProducts"
                                    @change="addProduct"
                                    @focus="loadProducts"
                                    :items="productsSugestions"
                                ></v-autocomplete>
                            </v-col>
                            <v-col cols="3">
                                <v-text-field
                                    label="Quantidade"
                                    type="number"
                                    required
                                    :disabled="productsMax[request.products[product]] === 0? true:false"
                                    :max="productsMax[request.products[product]]"
                                    min='1'
                                    :value="productsMax[request.products[product]] === 0? 0:1"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="3">
                                <v-text-field
                                    label="Disponível"
                                    type="number"
                                    required
                                    :value="productsMax[request.products[product]]"
                                    disabled
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols='6'>
                                <v-autocomplete
                                    label="Tipo de consumidor"
                                    :items="consumers"
                                ></v-autocomplete>
                            </v-col>
                            <v-col cols='6'>
                                <v-text-field
                                    label="Consumidor"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-textarea
                                    auto-grow
                                    filled 
                                    label="Observações"
                                    solo
                                >

                                </v-textarea>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-form>
                <v-card-actions>
                    <v-btn
                        color="primary"
                    >Solicitar</v-btn>
                    <v-btn
                        text
                        color="primary"
                        @click="clear"
                    >Cancelar</v-btn>                    
                </v-card-actions>
            </v-card>
        </v-row>
    </v-container>    
</template>
<script lang="ts">
import Vue from 'vue'
import app from '@/sdk';
export default {
    data(){
        return {
            products: [],
            loadingProducts: false,
            productsSugestions: [],
            consumers: [
                {
                    text: 'Usuário',
                    value: 'user',
                },
                {
                    text: 'Dentista',
                    value: 'dentist',
                },
                {
                    text: 'Consultório',
                    value: 'chamber',
                },
                {
                    text: 'Paciente',
                    value: 'patient',
                },
                {
                    text: 'Outro',
                    value: 'other',
                }
            ],
            productsMax: {},
            productsForms: [0],
            request: {
                products: [],
                note: '',
                consumer: {
                    type: '',
                    consumer: ''
                }
            }
        }
    },
    computed: {
        form(){
            return {
                products: this.request.products,
                note: this.request.note,
                consumer: {
                    type: this.request.consumer.type,
                    [this.request.consumer.type]: this.request.consumer.consumer
                }
            }
        }
    },
    mounted(){
        // this.loadProducts()
    },
    methods: {
        async clear(){
            this.$refs.form.reset()
            this.productsForms = [0]
        },
        async loadProducts(){
            if(this.productsSugestions||this.products === []){
                this.loadingProducts = true;
                app.categories.loadList()
                    .then(list => {
                        this.products = app.categories.list;
                        app.categories.list.forEach(product => {
                            this.productsSugestions.push({
                                text: product.name,
                                value: product.pk,
                            })
                            this.productsMax[product.pk] = product.amount;
                        });
                        this.loadingProducts = false;
                    })
            }               
        },
        ajustForms(){
            this.productsForms.forEach((item, index) => {
                this.productsForms[index] = index;
            })
        },
        async addProduct(){
            this.productsForms.push(this.productsForms.length)
        }
    },
}
</script>