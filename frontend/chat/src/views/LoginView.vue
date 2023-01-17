<template>
  <v-card class="mx-auto ma-8" width="800">

    <template v-slot:title> Login </template>
    <v-card-text>

      <v-form ref="form" v-model="valid" lazy-validation>
        <v-text-field
          v-model="username"
          :rules="usernameRules"
          label="Username"
          required
        ></v-text-field>

        <v-text-field
          v-model="password"
          :rules="passwordRules"
          label="Password"
          type="password"
          required
        ></v-text-field>

        <v-btn color="info" class="mr-4" @click="validate"> Login </v-btn>
        <v-btn color="info" class="mr-4" to="/register"> Register </v-btn>

      </v-form>
    </v-card-text>
  </v-card>
</template>


<script>
import axios from 'axios';

export default {
  data: () => ({
    valid: true,
    username: "",
    usernameRules: [
      (v) => !!v || "Username is required",
    ],
    password: "",
    passwordRules: [
      (v) => !!v || "Password is required",
    ],
  }),

  methods: {
    async validate() {
      const { valid } = await this.$refs.form.validate();

      if(valid){
        const data = {
            "username": this.username,
            "password": this.password
        }
        axios.post('http://localhost:8000/api/login', data)
        .then((response) => {
            const username = response.data.username;
            localStorage.setItem('username', username);

            this.$router.push('/');
        }).catch(() => {
            alert("Username or password wrong")
        });
      }
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
  },
};
</script>