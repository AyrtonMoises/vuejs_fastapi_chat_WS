<template>
  <v-card class="mx-auto ma-8" width="800">

    <template v-slot:title> Register </template>
    <v-btn color="info" class="ma-2" @click="$router.back()"> Back </v-btn>
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

        <v-btn color="info" class="mr-4" @click="validate"> Register </v-btn>
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
      (v) => (v && v.length >= 3) || "Username must be more than 2 character",
    ],
    password: "",
    passwordRules: [
      (v) => !!v || "Password is required",
      (v) => (v && v.length >= 3) || "Password must be more than 2 character",
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
        axios.post('http://localhost:8000/api/users', data)
        .then((response) => {
            alert(`User ${response.data.username} created with success`);
            this.$router.push('/login');
        });
      }

    }

  },
};
</script>