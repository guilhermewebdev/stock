<template>
    <v-form
        ref="form"
        autocomplete="off"
        @keypress.native.enter="submit"
    >
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
                        :rules="[rules.required]"
                        autocomplete="off"
                    ></v-text-field>
                </v-col>
                <v-col
                    class="px-0 pt-0"
                    cols="12"
                >
                    <v-text-field
                        v-model="form.email"
                        class="mt-0"
                        label='E-mail'
                        type="email"
                        name="input-10-1"
                        :rules="[rules.required, rules.min]"
                        hint="At least 8 characters"
                        autocomplete="off"
                        :aria-autocomplete="false"
                        counter
                    ></v-text-field>
                </v-col>
                <v-col
                    class="px-0 pt-0"
                    cols="12"
                >
                    <v-text-field
                        v-model="form.password1"
                        class="mt-0"
                        label='Crie uma senha'
                        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="show1 ? 'text' : 'password'"
                        name="input-10-1"
                        :rules="[rules.required, rules.min]"
                        hint="At least 8 characters"
                        autocomplete="off"
                        :aria-autocomplete="false"
                        counter
                        @click:append="show1 = !show1"
                    ></v-text-field>
                </v-col>
                <v-col
                    class="px-0 pt-0"
                    cols="12"
                >
                    <v-text-field
                        v-model="form.password2"
                        class="mt-0"
                        label='Confirme a senha'
                        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="show1 ? 'text' : 'password'"
                        name="input-10-1"
                        :rules="[rules.required, rules.min]"
                        hint="At least 8 characters"
                        autocomplete="off"
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
                        :loading="loading"
                    >
                        Cadastrar
                    </v-btn>
                </v-col>
            </v-row>
        </v-container>
    </v-form>
</template>
<script lang="ts">
import Vue from 'vue'
import app from '@/sdk';

export default Vue.extend({
    name: "form-register",
    data(){
        return {
            form: {},
            show1: false,
            rules: {
                required: v => !!v || "É preciso informar a senha",
                min: v => v.length >= 8 || "A senha deve conter pelo menos 8 caractéres"
            },
            loading:false,
        }
    },
    methods: {
        validate(){
            return this.$refs.form.validate()
        },
        toggleLoading(){
            this.loading = !this.loading;
        },
        notify(type, message){
            this.$emit('notify', type, message)
        },
        async submit() {
            this.toggleLoading()
            if(this.validate()){
                app.sessions.register(this.form)
                    .then(() => {
                        this.toggleLoading()
                        this.$router.push('/home')
                    })
                    .catch(err => {
                        this.toggleLoading()
                        this.$refs.form.value = false;
                        this.notify('danger', err.reponse.data)
                    })
            }
        },        
    },
})
</script>