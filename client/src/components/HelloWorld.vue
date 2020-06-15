<template>
    <v-container>
        <v-row class="text-center">
            <v-col cols="12">
                <v-img
                        :src="require('../assets/logo.svg')"
                        class="my-3"
                        contain
                        height="200"
                />
            </v-col>

            <v-col class="mb-4">
                <h1 class="display-2 font-weight-bold mb-3">
                    Welcome to Vuetify
                </h1>

                <p class="subheading font-weight-regular">
                    For help and collaboration with other Vuetify developers,
                    <br>please join our online
                    <a
                            href="https://community.vuetifyjs.com"
                            target="_blank"
                    >Discord Community</a>
                </p>
            </v-col>

            <v-col
                    class="mb-5"
                    cols="12"
            >
                <h2 class="headline font-weight-bold mb-3">
                    What's next?
                </h2>

                <v-row justify="center">
                    <a
                            v-for="(next, i) in whatsNext"
                            :key="i"
                            :href="next.href"
                            class="subheading mx-3"
                            target="_blank"
                    >
                        {{ next.text }}
                    </a>
                </v-row>

                <v-row justify="center">
                    <!--                    Message from server yiiiiiiiha: "{{socketMessage}}"-->


                </v-row>
                <v-btn variant="success" @click="sendMessage">Send message</v-btn>


            </v-col>

            <v-col
                    class="mb-5"
                    cols="12"
            >
                <h2 class="headline font-weight-bold mb-3">
                    Important Links
                </h2>

                <v-row justify="center">
                    <a
                            v-for="(link, i) in importantLinks"
                            :key="i"
                            :href="link.href"
                            class="subheading mx-3"
                            target="_blank"
                    >
                        {{ link.text }}
                    </a>
                </v-row>
            </v-col>

            <v-col
                    class="mb-5"
                    cols="12"
            >
                <h2 class="headline font-weight-bold mb-3">
                    Ecosystem
                </h2>

                <v-row justify="center">
                    <a
                            v-for="(eco, i) in ecosystem"
                            :key="i"
                            :href="eco.href"
                            class="subheading mx-3"
                            target="_blank"
                    >
                        {{ eco.text }}
                    </a>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
    import Vue from 'vue'
    import VueSocketIO from 'vue-socket.io'
    import SocketIO from "socket.io-client"


    Vue.use(new VueSocketIO({
            debug: true,
            connection: SocketIO('http://localhost:8050/'), //options object is Optional
        })
    );
    // const io = require('socket.io-client');
    import io from 'socket.io-client'

    export default {
        name: 'HelloWorld',

        data: () => ({
            socket: io,
            ecosystem: [
                {
                    text: 'vuetify-loader',
                    href: 'https://github.com/vuetifyjs/vuetify-loader',
                },
                {
                    text: 'github',
                    href: 'https://github.com/vuetifyjs/vuetify',
                },
                {
                    text: 'awesome-vuetify',
                    href: 'https://github.com/vuetifyjs/awesome-vuetify',
                },
            ],
            importantLinks: [
                {
                    text: 'Documentation',
                    href: 'https://vuetifyjs.com',
                },
                {
                    text: 'Chat',
                    href: 'https://community.vuetifyjs.com',
                },
                {
                    text: 'Made with Vuetify',
                    href: 'https://madewithvuejs.com/vuetify',
                },
                {
                    text: 'Twitter',
                    href: 'https://twitter.com/vuetifyjs',
                },
                {
                    text: 'Articles',
                    href: 'https://medium.com/vuetify',
                },
            ],
            whatsNext: [
                {
                    text: 'Explore components',
                    href: 'https://vuetifyjs.com/components/api-explorer',
                },
                {
                    text: 'Select a layout',
                    href: 'https://vuetifyjs.com/layout/pre-defined',
                },
                {
                    text: 'Frequently Asked Questions',
                    href: 'https://vuetifyjs.com/getting-started/frequently-asked-questions',
                },
            ],
        }),
        methods: {

            sendMessage(e) {

                console.log(e)
                this.$socket.emit('SEND_MESSAGE', {
                    msg: this.message
                });
                console.log('message sent to websocket server');

            },
        },

        created() {
            // test websocket connection
            const socket = io.connect('http://localhost:8050/');

            // getting data from server
            // eslint-disable-next-line
            socket.on('connect', function () {
                console.log('connected to webSocket');
                //sending to server
                socket.emit('my event', {data: 'I\'m connected!'});
            });

            // we have to use the arrow function to bind this in the function
            // so that we can access Vue  & its methods
            socket.on('update_on_layouts', (data) => {
                console.log(data);
            });
        },


        // mounted: function () {
        //     var socket = io('http://localhost:8050/');
        //     socket.on('heyhey', function () {
        //         console.log('COMING FROM THE SERVER')
        //         socket.emit('first-connect', 'A user has connected');
        //     })
        // },


        //
        // mounted() {
        //     this.io.on('message', (socket) => {
        //         console.log('COMING FROM THE SERVER')
        //         this.messages = JSON.parse(socket);
        //         console.log(JSON.parse(socket))
        //     })
        // }

        //
        // this.socket.on('message__', function () {
        //     console.log('THIS IS COMING FROM THE SERVER')
        //     this.socket.emit('first-connect', 'A user has connected');
        // })


        // {
        //     console.log('THIS IS COMING FROM THE SERVER')
        //     this.messages = JSON.parse(socket);
        //     console.log(JSON.parse(socket))
        // })
        // },


    }
</script>
