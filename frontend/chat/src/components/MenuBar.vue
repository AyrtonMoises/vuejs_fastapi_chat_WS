<template>
  <div>
    <v-toolbar
      color="info"
      
    >
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-app-bar-nav-icon
         v-bind="props"
        >
        </v-app-bar-nav-icon>
      </template>

      <v-list>
        <v-list-item to="/">Rooms</v-list-item>
        <v-list-item @click="logout">Logout</v-list-item>
      </v-list>
    </v-menu>
      <v-toolbar-title>Chat</v-toolbar-title>

      <v-spacer></v-spacer>


    </v-toolbar>
  </div>
</template>




<script>

export default {
  name: 'App',
  methods: {
    async logout(){
        localStorage.removeItem('username');
        this.username = "";
        this.$router.push('/login');
    }

  }
}

</script>
