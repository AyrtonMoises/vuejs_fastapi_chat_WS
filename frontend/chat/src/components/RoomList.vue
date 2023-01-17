<template>
  <div>
    <v-card class="mx-auto" :elevation="0">
      <v-list density="compact">
        <v-list-subheader>Rooms</v-list-subheader>

        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :value="item"
          active-color="success"
          :to="{
            name: 'room',
            params: {
              id: item.id,
            },
          }"
        >
          <template v-slot:prepend>
            <v-icon icon="mdi-home"></v-icon>
          </template>

          <v-list-item-title v-text="item.title"></v-list-item-title>
        </v-list-item>
      </v-list>

    </v-card>

    <RoomCreate />


  </div>
</template>


<script>
import axios from "axios";
import RoomCreate from '../components/RoomCreate.vue';


export default {
  name: "Rooms",
  data() {
    return {
      dialog: false,
      items: [],
    };
  },
  components: {
    RoomCreate
  },
  methods: {
    async getRooms() {
      axios.get("http://localhost:8000/api/rooms").then((response) => {
        this.items = response.data;
      });
    },
  },
  mounted() {
    this.getRooms();
  },
};
</script>