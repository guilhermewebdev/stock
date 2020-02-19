<template>
    <v-container>
        <v-row
            align="center"
            justify="center"
        >
            <v-col
                cols="12"
                xm="12"
                sm="6"
                md="5"
                lg='5'
                xl='3'
            >
                <v-tabs
                    centered
                    grow
                    v-if="!isAuth"
                >
                    <v-tab>Entrar</v-tab>
                    <v-tab>Cadastrar</v-tab>
                    <v-tab-item>
                        <form-login></form-login>
                    </v-tab-item>
                    <v-tab-item>
                        <form-register></form-register>
                    </v-tab-item>
                </v-tabs>
            </v-col>
        </v-row>
    </v-container>
</template>
<script lang="ts">
import Vue from 'vue'
import app from '../sdk';
import FormLogin from '@/components/forms/Login.vue'
import FormRegister from '@/components/forms/Register.vue';
export default Vue.extend({
    data(){
        return {
            sdk: app, 
        }
    },
    computed: {
        isAuth(){
            return this.$store.state.isAuthenticated;
        }
    },
    components: {
        FormLogin,
        FormRegister
    }
})
</script>