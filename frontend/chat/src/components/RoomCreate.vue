<template>
<v-dialog
    v-model="dialog"
>
    <template v-slot:activator="{ props }">
        <v-col>
    <v-btn icon="mdi-plus" color="primary" v-bind="props"></v-btn>
    </v-col>

    </template>

  <v-card class="mx-auto ma-8" width="800">

    <template v-slot:title> Create Room </template>
    <v-card-text>

      <v-form ref="form" v-model="valid" lazy-validation>
        <v-text-field
          v-model="title"
          :rules="titleRules"
          label="Title"
          required
        ></v-text-field>

        <v-btn color="info" class="mr-4" @click="validate"> Create </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</v-dialog>
</template>


<script>

import axios from 'axios';


export default {
name: "RoomCreate",
  data: () => ({
    dialog: false,
    valid: true,
    title: "",
    titleRules: [
      (v) => !!v || "Room is required",
      (v) => (v && v.length >= 3) || "Room must be more than 2 character",
    ]
  }),

  methods: {
    async validate() {
      const { valid } = await this.$refs.form.validate();

      if(valid){
        const data = {
            "title": this.title,
        }
        axios.post('http://localhost:8000/api/rooms', data)
        .then(() => {
            this.dialog = false,
            this.$refs.form.reset();
            this.$parent.getRooms();
        });
      }

    },

  },
};

</script>