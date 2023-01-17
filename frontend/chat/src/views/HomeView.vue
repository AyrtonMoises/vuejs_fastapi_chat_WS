<template>
  <div>
  <RoomList />
  </div>
</template>

<script>
import { defineComponent } from 'vue';

// Components
import RoomList from '../components/RoomList.vue';

export default defineComponent({
  name: 'HomeView',
  components: {
    RoomList
  },
});

</script>
