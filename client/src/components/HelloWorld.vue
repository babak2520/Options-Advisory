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

                    name: this.stock,
                    data: this.generateDayWiseTimeSeries() ,
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
                        type: 'date',
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
            //generateDayWiseTimeSeries(s, count) {
                generateDayWiseTimeSeries() {
                // var values = [[
                //     4, 3, 10, 9, 29, 19, 25, 9, 12, 7, 19, 5, 13, 9, 17, 2, 7, 5
                // ], [
                //     2, 3, 8, 7, 22, 16, 23, 7, 11, 5, 12, 5, 10, 4, 15, 2, 6, 2
                // ]];
                // console.log("called generatedaywise function")
                // var i = 0;
                // var series = [];
                // var x = new Date("11 Nov 2012").getTime();
                // while (i < count) {
                //     series.push([x, values[s][i]]);
                //     x += 86400000;
                //     i++;
                // }
                console.log("here is the data inside generate function:")
                console.log(this.plot_data)
                var series = this.plot_data
                return series;
            }

        },

        mounted: function () {
            //console.log("mounted function is called")
            let self = this
            var socket = io.connect('localhost:8050');
            socket.on('message_to_client', function (d) {
                    self.item['name'] = d["data"]
                },
            )
            socket.on('plot_data_from_server', function (data) {
                    console.log('this is the data to be plotted:')
                    // console.log(data.data)
                    // var dict = [];
                    // dict = data.data['Close']
                    for (var key in data.data){
                        console.log(key, data.data[key])
//                         for (var fuckthis in key){
// console.log('hereee',fuckthis)
//                         }
                    }


// axios.get(path).then(jsonfiles => {

//           let results = jsonfiles.data
//           let deptresult = results['DEPT']
//           let hdthresult = results['HDTH']
//           let datetimeresult = results['Date/Time']

//           this.DEPT = JSON.parse(deptresult)
//           this.HDTH = JSON.parse(hdthresult)
//           this.datetime = JSON.parse(datetimeresult)
//           var depths = [];
//           var hdths = [];
//           for (var i = 0; i < this.DEPT.length && i < this.HDTH.length; i++) {
//             depths[i] = [(new Date(this.datetime[i])), this.DEPT[i]];
//             hdths[i] = [(new Date(this.datetime[i])), this.HDTH[i]];
//           }




                    // for (var i = 0; i < this.channel.length; i++) {
                    //     related_channel[i] = [(new Date(this.datetime_[i])), this.channel[i]];
                    //   }
                    //const obj = JSON.parse(data.data['Close']);
                    //console.log(obj)

                },
            )

        }
    }
</script>
