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
                    @keypress.native.enter="submit"
                >
                    <v-container>
                        <v-row v-for="(product, index) in request.products" :key="index">
                            <v-col cols="6">
                                <v-autocomplete
                                    label="Produto"
                                    required
                                    autofocus
                                    :rules="[rules.required]"
                                    @click:append-outer="request.products.splice(index, 1);"
                                    :append-outer-icon="(index > 0)?'mdi-close':''"
                                    v-model="product.product"
                                    :loading="loadingProducts"
                                    @change="addProduct(index), product.amount = productsMax[product.product]==0?0:product.amount"
                                    @blur.once="removeVoidProduct(index)"
                                    @focus="loadProducts"
                                    :items="productsSugestions"
                                ></v-autocomplete>
                            </v-col>
                            <v-col cols="3">
                                <v-text-field
                                    label="Quantidade"
                                    type="number"
                                    v-model="product.amount"
                                    required
                                    :disabled="productsMax[product.product] === 0? true:false"
                                    :max="productsMax[product.product]"
                                    min='1'
                                    :value="productsMax[product.product]==0?0:1"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="3">
                                <v-text-field
                                    label="Disponível"
                                    type="number"
                                    :value="productsMax[product.product]"
                                    disabled
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row v-if="addButton">
                            <v-col cols="3">
                                <v-btn
                                    @click="addProduct(request.products.length - 1)"
                                >Adicionar</v-btn>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols='6'>
                                <v-autocomplete
                                    label="Tipo de consumidor"
                                    :rules="[rules.required]"
                                    :items="consumers"
                                    v-model="request.consumer.type"
                                ></v-autocomplete>
                            </v-col>
                            <v-col cols='6'>
                                <v-text-field
                                    :rules="[rules.required]"
                                    v-model="request.consumer.consumer"
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
                                    @keypress.native.enter.stop
                                >
                                </v-textarea>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-form>
                <v-card-actions>
                    <v-btn
                        color="primary"
                        @click="submit"
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
            rules: {
                required: v => !!v || 'É preciso preencher o campo!'
            },
            request: {
                products: [
                    {
                        product: null,
                        amount: 1,
                    }
                ],
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
        },
        addButton(){
            return Boolean(this.request.products[this.request.products.length - 1].product || false)
        },
    },
    methods: {
        async clear(){
            this.$refs.form.reset()
            this.$data.request = {
                products: [
                    {
                        product: null,
                        amount: 1,
                    }
                ],
                note: '',
                consumer: {
                    type: '',
                    consumer: '',
                }
            }
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
        async submit(){
            if(this.$refs.form.validate()){
                console.log(this.form)
                app.requests.consum.createItem(this.form)
                    .then(() => alert('Enviado!'))
                    .catch(err => console.log(err.response.data))
            }
        },
        async addProduct(product:number){
            console.log(this.request.products)
            if(product === (this.request.products.length-1)){
                this.request.products.push({
                        product: null,
                        amount: 1,
                })
                console.log(this.request.products)
            }
        },
        async removeVoidProduct(index:number){
            if(!this.addButton && (index === (this.request.products.length - 1)) && index > 0){
                this.request.products.splice(index, 1);
            }
        }
    },
}
</script>