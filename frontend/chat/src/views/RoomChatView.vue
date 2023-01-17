<template>
  <div id="messages">

    <v-container>
      <div  v-for="i in messages" :key="i">
      
      <v-row no-gutters style="margin-top: 20px" justify="start" v-if="current_user !== i.username">
        <v-col
          class="pa-2 bg-grey rounded-xl rounded-bs-0"
          align-self="start"
          cols="7"
        >
          <div class="ma-2">
            <div class="text-h6">{{i.username}}</div>
            <p>{{i.message}}</p>
          </div>
        </v-col>
      </v-row>

      <v-row no-gutters style="margin-top: 20px" justify="end" v-else>
        <v-col
          class="pa-4 bg-pink rounded-xl rounded-be-0"
          align-self="end"
          cols="7"
        >
          <div class="ma-2">
            <div class="text-h6">{{i.username}}</div>
            <p>{{i.message}}</p>
          </div>
        </v-col>
      </v-row>
      </div>
    </v-container>

    <v-card :elevation="0">
      <v-card-text>
        <v-form ref="form" v-model="valid" lazy-validation @submit.prevent>
          <v-text-field
            v-model="message"
            label="Message"
            :rules="messageRules"
            required
          ></v-text-field>

          <v-btn color="info" class="mr-4" @click="sendMessage"> Send </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>


<script>
export default {
  name: "App",
  data() {
    return {
      socket: {},
      message: "",
      messages: [],
      current_user: localStorage.getItem("username"),
      room_id: window.location.pathname.split("/")[2],
      messageRules: [(v) => !!v || "Message is required"],
    };
  },
  async mounted() {
    const socketProtocol =
      window.location.protocol === "https:" ? "wss:" : "ws:";
    const port = ":8000";
    const echoSocketUrl =
      socketProtocol +
      "//" +
      window.location.hostname +
      port +
      "/ws/" +
      this.room_id;

    // Define socket and attach it to our data object
    this.socket = await new WebSocket(echoSocketUrl);
    // When it opens, console log that it has opened
    this.socket.onopen = () => {
      console.log("Websocket connected.");
    };
    // When we receive a message from the server, we can capture it here in the onmessage event.
    this.socket.onmessage = (event) => {
      // We can parse the data we know to be JSON, and then check it for data attributes
      let parsedMessage = JSON.parse(event.data);
      // If those data attributes exist, we can then console log or show data to the user on their web page.
      this.messages.push(parsedMessage);
      window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);

    };
  },
  updated() {
      // whenever data changes and the component re-renders, this is called.
      this.$nextTick(() => this.scrollToEnd());
  },
  methods: {
    async waitForOpenConnection() {
      return new Promise((resolve, reject) => {
        const maxNumberOfAttempts = 5;
        const intervalTime = 200;
        let currentAttempt = 0;
        const interval = setInterval(() => {
          if (currentAttempt > maxNumberOfAttempts - 1) {
            clearInterval(interval);
            reject(new Error("Maximum number of attempts exceeded."));
          } else if (this.socket.readyState === this.socket.OPEN) {
            clearInterval(interval);
            resolve();
          }
          currentAttempt++;
        }, intervalTime);
      });
    },
    async sendMessage() {
      const { valid } = await this.$refs.form.validate();

      if (valid) {
        if (this.socket.readyState === this.socket.OPEN) {
          try {
            await this.waitForOpenConnection(this.socket);
            var message_obj = {
              message: this.message,
              username: this.current_user,
            };
            this.socket.send(JSON.stringify(message_obj));
            this.message = "";
            this.$refs.form.reset();
          } catch (err) {
            console.error(err);
          }
        } else {
          console.log("Not connected");
        }
      }
    },
    scrollToEnd: function () {
        // scroll to the start of the last message
        this.$el.scrollTop = this.$el.lastElementChild.offsetTop;
    }
  },
};
</script>
