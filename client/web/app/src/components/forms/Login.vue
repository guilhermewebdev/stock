<template>
    <v-form ref="form">
        <v-container fluid>
            <v-row>
                <v-col
                    class="px-0 pt-0"
                    cols="12"
                >
                    <v-text-field
                        v-model="form.username"
                        label='Nome de usuário'
                        class="mt-0"
                    ></v-text-field>
                </v-col>
                <v-col
                    class="px-0 pt-0"
                    cols="12"
                >
                    <v-text-field
                        v-model="form.password"
                        class="mt-0"
                        label='Senha'
                        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        :rules="[rules.required, rules.min]"
                        :type="show1 ? 'text' : 'password'"
                        name="input-10-1"
                        hint="At least 8 characters"
                        :aria-autocomplete="false"
                        counter
                        @click:append="show1 = !show1"
                    ></v-text-field>
                </v-col>
                <v-col
                    class="px-0 pt-0"
                >
                    <v-btn 
                        block
                        color="primary"
                        @click="submit"
                    >
                        Entrar
                    </v-btn>
                </v-col>
            </v-row>
        </v-container>
    </v-form>
</template>
<script lang="ts">
import Vue from 'vue';
import connect from '@/connect';
export default Vue.extend({
    name: 'form-login',
    data(){
        return {
            form: {},
            show1: false,
            rules: {
                required: v => !!v || "É preciso informar a senha",
                min: v => v >= 8 || "A senha deve conter pelo menos 8 caractéres"
            }
        }
    },
    methods: {
        validate(){
            return this.$refs.form.validate()
        },
        async submit() {
            if(this.validate()){
                connect.post('/sessions/login.json', this.form)
                .then((result) => {
                    alert(result)
                }).catch((err) => {
                    alert(err)
                });
            }
        }
    }
})
</script>