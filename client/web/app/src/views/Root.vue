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
                >
                    <v-tab>Entrar</v-tab>
                    <v-tab>Cadastrar</v-tab>
                    <v-tab-item>
                        <form-login></form-login>
                    </v-tab-item>
                </v-tabs>
            </v-col>
        </v-row>
    </v-container>
</template>
<script lang="ts">
import Vue from 'vue'
import FormLogin from '@/components/forms/Login.vue'
export default Vue.extend({
    components: {
        FormLogin
    }
})
</script>