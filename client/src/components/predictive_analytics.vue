<template>
  <v-data-table dark
                :headers="headers"
                :items="items"
                hide-actions
                item-key="identifier_name"
  >
    <template slot="items" slot-scope="props">
      <tr @click="props.expanded = !props.expanded">
        <td>{{ props.item.identifier_name }}</td>
      </tr>
    </template>
    <template slot="expand" slot-scope="props">

      <div v-if="props.item.identifier_name === 'Dynamic time warping'">

        <v-card flat>

          <v-card flat="flat" color=dark>

            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-progress-linear slot="progress" color="#41b883" determinate value=20></v-progress-linear>

              <v-layout row="row" wrap="wrap">

                <v-flex sm3="sm3">
                  <v-text-field label="New Channel Name" v-model="props.item.name"></v-text-field>
                </v-flex>
                <div class="col-3">

                  <label class="typo__label"><font color='#d9d9e2'>Choose a channel</font></label>
                  <multiselect
                    v-model="multiSelectOptions.value"
                    :options="multiSelectOptions.options"
                    :custom-label="customLabel"
                    :multiple="false"
                    placeholder="Select one"
                    label="channel_name"
                    track-by="channel_name"
                    id="multiselect"
                    @input="onChange"
                  ></multiselect>
                </div>

                <v-flex sm3="sm3">
                  <div class="vdatetime">
                    <label class="typo__label"><font color='#d9d9e2'>Choose start date/time</font></label>
                    <div></div>
                    <v-input id="start time" type="text" class="vdatetime-input-start" dark>
                      <datetime type="datetime" v-model="start_time" format="yyyy-MM-dd HH:mm:ss" auto
                                class="theme-green">
                      </datetime>
                    </v-input>
                  </div>
                </v-flex>

                <v-flex sm3="sm3">
                  <div class="vdatetime">
                    <label class="typo__label"><font color='#d9d9e2'>Choose end date/time</font></label>
                    <div></div>
                    <v-input id="end time" type="text" class="vdatetime-input-end" dark>
                      <datetime type="datetime" v-model="end_time" format="yyyy-MM-dd HH:mm:ss" auto
                                class="theme-green">
                      </datetime>
                    </v-input>
                  </div>
                </v-flex>

                <v-flex sm3="sm3">
                  <v-text-field label="Step Size" v-model="props.item.step_size"></v-text-field>
                </v-flex>

                <v-flex sm3="sm3">
                  <v-text-field label="Radius" v-model="props.item.radius"></v-text-field>
                </v-flex>
                <span v-if="!props.item.is_fiscal">
                      <v-btn
                        @click='statusChanged'>compute
                      </v-btn>
              </span>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>

      <div v-if="props.item.identifier_name === 'Changepoint detection'">

        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-flex sm3="sm3">
                  <v-text-field label="New Channel Name" v-model="props.item.name"></v-text-field>
                </v-flex>
                <div class="col-3">

                  <label class="typo__label"><font color='#d9d9e2'>Choose a channel</font></label>
                  <multiselect
                    v-model="multiSelectOptions.value"
                    :options="multiSelectOptions.options"
                    :custom-label="customLabel"
                    :multiple="false"
                    placeholder="Select one"
                    label="channel_name"
                    track-by="channel_name"
                    id="multiselect_changepoint"
                    @input="onChange"
                  ></multiselect>
                </div>

                <v-flex sm3="sm3">
                  <v-text-field label="Wait for Sample Amount" v-model="props.item.wait_for_samples"></v-text-field>
                </v-flex>

                <v-flex sm3="sm3">
                  <v-text-field label="Alpha" v-model="props.item.alpha"></v-text-field>
                </v-flex>
                <v-flex sm3="sm3">
                  <v-text-field label="Beta" v-model="props.item.beta"></v-text-field>
                </v-flex>
                <v-flex sm3="sm3">
                  <v-text-field label="Kappa" v-model="props.item.kappa"></v-text-field>
                </v-flex>
                <v-flex sm3="sm3">
                  <v-text-field label="Mu" v-model="props.item.Mu"></v-text-field>
                </v-flex>

                <v-btn
                  @click='statusChanged_changepoint'>compute
                </v-btn>

                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>

      </div>

      <div v-if="props.item.identifier_name === 'Mechanical specific energy'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>

      <div v-if="props.item.identifier_name === 'Gaussian processes'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>



      <div v-if="props.item.identifier_name === 'Neural networks'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>



      <div v-if="props.item.identifier_name === 'Random forest regression'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>



      <div v-if="props.item.identifier_name === 'Support vector machines'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>


      <div v-if="props.item.identifier_name === 'Genetic algorithms'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>


      <div v-if="props.item.identifier_name === 'Deep learning'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>


      <div v-if="props.item.identifier_name === 'Gaussian mixture model'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>


      <div v-if="props.item.identifier_name === 'Deep learning'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>


      <div v-if="props.item.identifier_name === 'Gaussian mixture model'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>

      <div v-if="props.item.identifier_name === 'Reinforcement learning'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>

      <div v-if="props.item.identifier_name === 'Hydraulics model'">
      <v-card flat>
        <v-card flat="flat" color=dark>
          <v-container fluid="fluid" grid-list-xl="grid-list-xl">
            <v-layout row="row" wrap="wrap">
              <v-btn
                @click='statusChanged_mse'>compute
              </v-btn>
              <v-flex fill-height d-flex xs12>
                <v-card dark tile flat>
                </v-card>
              </v-flex>
              <v-flex fill-height d-flex xs12>
                <v-card dark tile flat>
                </v-card>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-card>
    </div>

      <div v-if="props.item.identifier_name === 'Hydraulics model - swab and surge'">
      <v-card flat>
        <v-card flat="flat" color=dark>
          <v-container fluid="fluid" grid-list-xl="grid-list-xl">
            <v-layout row="row" wrap="wrap">
              <v-btn
                @click='statusChanged_mse'>compute
              </v-btn>
              <v-flex fill-height d-flex xs12>
                <v-card dark tile flat>
                </v-card>
              </v-flex>
              <v-flex fill-height d-flex xs12>
                <v-card dark tile flat>
                </v-card>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-card>
    </div>



      <div v-if="props.item.identifier_name === 'Torque and drag model'">
      <v-card flat>
        <v-card flat="flat" color=dark>
          <v-container fluid="fluid" grid-list-xl="grid-list-xl">
            <v-layout row="row" wrap="wrap">
              <v-btn
                @click='statusChanged_mse'>compute
              </v-btn>
              <v-flex fill-height d-flex xs12>
                <v-card dark tile flat>
                </v-card>
              </v-flex>
              <v-flex fill-height d-flex xs12>
                <v-card dark tile flat>
                </v-card>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-card>
    </div>



      <div v-if="props.item.identifier_name === 'Hole cleaning model'">
      <v-card flat>
        <v-card flat="flat" color=dark>
          <v-container fluid="fluid" grid-list-xl="grid-list-xl">
            <v-layout row="row" wrap="wrap">
              <v-btn
                @click='statusChanged_mse'>compute
              </v-btn>
              <v-flex fill-height d-flex xs12>
                <v-card dark tile flat>
                </v-card>
              </v-flex>
              <v-flex fill-height d-flex xs12>
                <v-card dark tile flat>
                </v-card>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-card>
    </div>

      <div v-if="props.item.identifier_name === 'BHA optimization'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>


      <div v-if="props.item.identifier_name === 'Washout detection'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>


      <div v-if="props.item.identifier_name === 'Directional drilling KPIs'">
        <v-card flat>
          <v-card flat="flat" color=dark>
            <v-container fluid="fluid" grid-list-xl="grid-list-xl">
              <v-layout row="row" wrap="wrap">
                <v-btn
                  @click='statusChanged_mse'>compute
                </v-btn>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
                <v-flex fill-height d-flex xs12>
                  <v-card dark tile flat>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card>
        </v-card>
      </div>

    </template>
  </v-data-table>
</template>

<style src="../assets/css/datetimepicker_costum.css"></style>


<script>
  import Vue from 'vue'
  import Vuetify from 'vuetify'
  import {BaseTable} from "@/components";
  import '../plugins/vuetify'
  import axios from 'axios'
  import 'vue-datetime/dist/vue-datetime.css'

  document.body.setAttribute('data-app', true)
  Vue.use(Vuetify);
  import '../stylus/main.styl'
  import Multiselect from 'vue-multiselect'
  import {Datetime} from 'vue-datetime';


  export default {
    name: 'predictive',
    components: {
      BaseTable,
      Multiselect,
      datetime: Datetime
    },
    data() {
      return {
        start_time: "2018-12-12 10:05:02",
        end_time: "2018-12-12 11:05:02",

        multiSelectOptions: {
          value: [],
          options: []
        },
        headers: [
          {
            text: 'Computations',
            align: 'left',
            sortable: false,
            value: 'identifier_name'
          },
        ],
        items: [
          {
            value: false,
            identifier_name: 'Dynamic time warping',
            name: null,
            step_size: 10,
            datetime13: "2018-12-12 10:05:02",
            radius: 5,

          },
          {
            value: false,
            identifier_name: 'Changepoint detection',
            name: null,
            wait_for_samples: 20,
            alpha: 0.1,
            beta: 0.01,
            kappa: 1,
            Mu: 0,
          },
          {
            value: false,
            identifier_name: 'Mechanical specific energy',
          },
          {
            value: false,
            identifier_name: 'Gaussian processes',
          },
          {
            value: false,
            identifier_name: 'Neural networks',
          },
          {
            value: false,
            identifier_name: 'Random forest regression',
          },
          {
            value: false,
            identifier_name: 'Support vector machines',
          },
          {
            value: false,
            identifier_name: 'Genetic algorithms',
          },
          {
            value: false,
            identifier_name: 'Deep learning',
          },
          {
            value: false,
            identifier_name: 'Gaussian mixture model',
          },
          {
            value: false,
            identifier_name: 'Reinforcement learning',
          },
          {
            value: false,
            identifier_name: 'Hydraulics model',
          },
          {
            value: false,
            identifier_name: 'Hydraulics model - swab and surge',
          },
          {
            value: false,
            identifier_name: 'Torque and drag model',
          },
          {
            value: false,
            identifier_name: 'Hole cleaning model',
          },
          {
            value: false,
            identifier_name: 'BHA optimization',
          },
          {
            value: false,
            identifier_name: 'Washout detection',
          },
          {
            value: false,
            identifier_name: 'Directional drilling KPIs',
          },

        ]
      }
    },
    created() {
      this.initialize_dropdown()
    },

    watch: {
      start_time: function (val, oldVal) {
        this.start_datetime = val
      },
      end_time: function (val, oldVal) {
        this.end_datetime = val
      },

    },

    methods:
      {

        statusChanged: function (event) {

          this.new_channel_name = this.items[0].name
          this.step_size = this.items[0].step_size
          this.radius = this.items[0].radius
          var dict = [];
          dict.push({
            new_channel_name: this.new_channel_name,
            selected_channel: this.selected_channel,
            start_datetime: this.start_datetime,
            end_datetime: this.end_datetime,
            step_size: this.step_size,
            radius: this.radius,
          });
          axios.post('http://localhost:8050/table_list', {
            dict
          })
            .then(response => {
              this.initialize_dropdown()
            }).catch(function (error) {
            console.log(error);
          });


        },

        statusChanged_changepoint: function (event) {

          this.new_channel_name = this.items[1].name
          this.wait_for_samples = this.items[1].wait_for_samples
          this.alpha = this.items[1].alpha
          this.beta = this.items[1].beta
          this.kappa = this.items[1].kappa
          this.Mu = this.items[1].Mu
          var dict = [];
          dict.push({
            new_channel_name: this.new_channel_name,
            selected_channel: this.selected_channel,
            wait_for_samples: this.wait_for_samples,
            alpha: this.alpha,
            beta: this.beta,
            kappa: this.kappa,
            Mu: this.Mu,
          });
          axios.post('http://localhost:8050/calculate_changepoint', {
            dict
          })
            .then(response => {
              this.initialize_dropdown()
            }).catch(function (error) {
            console.log(error);
          });


        },

        statusChanged_mse() {
          const path = 'http://localhost:8050/calculate_mse';
          axios.get(path).then(jsonfiles => {

            this.initialize_dropdown()

          })
            .catch(error => {
              console.log(error)
            })

        },


        initialize_dropdown() {
          const path = 'http://localhost:8050/visualize';
          axios.get(path).then(jsonfiles => {
            let channel_names = jsonfiles.data;
            var new_options = [];
            channel_names.forEach(function (channel) {
              new_options.push({
                unit: "",
                channel_name: channel
              });
            });
            this.multiSelectOptions = {
              value: [],
              options: new_options
            }
          })
            .catch(error => {
              console.log(error)
            })
        },
        customLabel(option) {
          return `${option.channel_name} ${option.unit}`
        },
        onChange: function (selected_channel) {

          this.selected_channel = selected_channel
        }
        ,
      },
  }
</script>
