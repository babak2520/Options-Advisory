<template>
    <v-main>
        <v-row
                :align="alignment"
                :justify="justify"
                class="grey lighten-5">
            <v-col cols="12" sm="6">
                <v-btn variant="success" @click="sendMessage">Send message to server</v-btn>
            </v-col>
            <v-col cols="12" sm="6">
                <v-text-field
                        label=""
                        v-model="item.name"
                        single-line
                        outlined
                ></v-text-field>
            </v-col>
        </v-row>

        <v-col sm="6">
            <div id="chart">
                <apexchart type="area" height="350" :options="chartOptions" :series="series"></apexchart>
            </div>
        </v-col>

    </v-main>
</template>

<script>
    const io = require('socket.io-client');
    import VueApexCharts from 'vue-apexcharts'

    export default {
        name: 'HelloWorld',
        components: {
            apexchart: VueApexCharts,
        },
        data() {
            return {
                alignment: 'center',
                justify: 'center',
                item:
                    {
                        name: "click button for server to send message",
                    },
                series: [{
                    name: 'XYZ MOTORS',
                    data: this.generateDayWiseTimeSeries(0, 18)
                }],
                chartOptions: {
                    chart: {
                        type: 'area',
                        stacked: false,
                        height: 350,
                        zoom: {
                            type: 'x',
                            enabled: true,
                            autoScaleYaxis: true
                        },
                        toolbar: {
                            autoSelected: 'zoom'
                        }
                    },
                    dataLabels: {
                        enabled: false
                    },
                    markers: {
                        size: 0,
                    },
                    title: {
                        text: 'Option Price Prediction',
                        align: 'left'
                    },
                    fill: {
                        type: 'gradient',
                        gradient: {
                            shadeIntensity: 1,
                            inverseColors: false,
                            opacityFrom: 0.5,
                            opacityTo: 0,
                            stops: [0, 90, 100]
                        },
                    },
                    yaxis: {
                        labels: {
                            formatter: function (val) {
                                return (val / 1000000).toFixed(0);
                            },
                        },
                        title: {
                            text: 'Price'
                        },
                    },
                    xaxis: {
                        type: 'datetime',
                    },
                    tooltip: {
                        shared: false,
                        y: {
                            formatter: function (val) {
                                return (val / 1000000).toFixed(0)
                            }
                        }
                    }
                },
            }
        },

        methods: {
            sendMessage(e) {
                var socket = io.connect('localhost:8050');

                console.log(e)
                socket.emit('SEND_MESSAGE', {
                    msg: this.message
                });
                console.log('message sent to websocket server');
            },
            generateDayWiseTimeSeries(s, count) {
                var values = [[
                    4, 3, 10, 9, 29, 19, 25, 9, 12, 7, 19, 5, 13, 9, 17, 2, 7, 5
                ], [
                    2, 3, 8, 7, 22, 16, 23, 7, 11, 5, 12, 5, 10, 4, 15, 2, 6, 2
                ]];
                var i = 0;
                var series = [];
                var x = new Date("11 Nov 2012").getTime();
                while (i < count) {
                    series.push([x, values[s][i]]);
                    x += 86400000;
                    i++;
                }
                return series;
            }

        },

        created: function () {
            var socket = io.connect('localhost:8050');
            setInterval(function () {
                socket.emit('ping', {
                    msg: this.message
                });
                console.log('is the session alive ?')
            }, 10000);
            socket.on('pong', function () {
                console.log('session is alive')
            })

        },
        mounted: function () {
            let self = this
            var socket = io.connect('localhost:8050');
            socket.on('message_to_client', function (d) {
                    self.item['name'] = d["data"]
                },
            )
            socket.on('plot_data_from_server', function (data) {

                    console.log(data)

                },
            )

        }
    }
</script>
