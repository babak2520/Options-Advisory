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

        <div class="example">

            <v-col sm2="sm2">
                <v-card ref="form">
                    <v-card-text>

                        <v-autocomplete
                                ref="stock"
                                v-model="stock"
                                :rules="[() => !!stock || 'This field is required']"
                                :items="stocks"
                                label="Stock"
                                placeholder="Select..."
                                required
                        ></v-autocomplete>

                        <label class="typo__label"><font color='black'>Choose desired projection
                            date</font></label>
                        <v-input id="desired projection date" type="text" class="vdatetime-input-end" dark>
                            <date-pick type="date" ref="desired_projection_date" v-model="desired_projection_date"
                                      format="'YYYY.MM.DD'"
                                      auto
                                      class="theme-orange"></date-pick>
                        </v-input>

                        <v-text-field :rules="rules"
                                      label="Enter the lookback amount"
                                      placeholder="i.e. 200"
                                      ref="lookback"
                                      v-model="lookback"
                                      type="number" 
                        ></v-text-field>


                    </v-card-text>
                    <v-divider class="mt-12"></v-divider>
                    <v-card-actions>
                        <v-btn text>Cancel</v-btn>
                        <v-spacer></v-spacer>
                        <v-slide-x-reverse-transition>

                        </v-slide-x-reverse-transition>


                        <v-btn variant="success" @click="submit">Estimate the Projection</v-btn>


                    </v-card-actions>
                </v-card>
            </v-col>

            <v-col sm="8">
                <div id="chart">
                    <apexchart type="area" height="350" :options="chartOptions" :series="series"></apexchart>
                </div>
            </v-col>

        </div>

    </v-main>
</template>
<style src="../assets/css/vueDatePick.css"></style>

<script>
    const io = require('socket.io-client');
    import VueApexCharts from 'vue-apexcharts'
    //import Vue from 'vue'
    //import {Datetime} from 'vue-datetime'
    // You need a specific loader for CSS files
    //import 'vue-datetime/dist/vue-datetime.css'
    import DatePick from 'vue-date-pick';

    //Vue.use(Datetime)


    export default {
        name: 'HelloWorld',
        components: {
            apexchart: VueApexCharts,
            DatePick,
        },
        data() {
            return {
                stock: null,
                stocks: ['EOG', 'SLB'],
                formHasErrors: false,
                desired_projection_date: null,
                lookback: null,
                // plotdata: [],

                rules: [
                    value => !!value || 'Required.',
                    value => (value || '').length <= 20 || 'Max 20 characters',
                    value => value < 1000 || 'Value needs to be below 1000',
                    value => value > 0 || 'Value needs to be above 0'
                ],

                alignment: 'center',
                justify: 'center',
                item:
                    {
                        name: "click button for server to send message",
                    },
                series: [{

                    name: 'XYZ MOTORS',
                    data: this.plotdata, 

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

        computed: {
            form() {
                return {
                    stock: this.stock,
                    desired_projection_date: this.desired_projection_date,
                    lookback: this.lookback,
                }
            },
        },

        methods: {
            // ToDo, make th reset button work
            // resetForm() {
            //     this.errorMessages = []
            //     this.formHasErrors = false
            //
            //     Object.keys(this.form).forEach(f => {
            //         this.$refs[f].reset()
            //     })
            // },
            submit() {
                var socket = io.connect('localhost:8050');
                this.formHasErrors = false
                Object.keys(this.form).forEach(f => {
                    if (!this.form[f]) {
                        this.formHasErrors = true
                        alert('Please fill the form with correct information')
                    }
                },)
                // if the form checks out, submit the data
                if (!this.formHasErrors) {
                    console.log(this.form)
                    socket.emit('client_gives_form_data', {
                        data: this.form
                    });
                }
            },

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
                console.log(series)
                return series;
            }

        },





        mounted: function () {
            let self = this
            var socket = io.connect('localhost:8050');
            socket.on('message_to_client', function (d) {
                    self.item['name'] = d["data"]
                },
            )
            socket.on('plot_data_from_server', function (data) {
                    console.log('inside mounted function socket.on')
                    var parsedData = JSON.parse(data.data)
                    this.plotdata =[]
                    //console.log(parsedData)
                    for (const [key, value] of Object.entries(parsedData)) {
                        let date = new Date(key).getTime()
                        this.plotdata.push([date, value['Actual or Pred Close']])
                    }
                    console.log(this.plotdata)

                }.bind(this)
                
            )
            // this.plotdata = self.plotdata
            // console.log('youre at the end of mounted block')
            // console.log(this.plotdata)
        },



    }
    
</script>
