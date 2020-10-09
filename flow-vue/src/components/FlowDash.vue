<template>
  <div class="row" v-if="stockData.length>0">
    <!-- Two thirds of the screen's width for the chart element -->
    <div class="col-8" >
      <linechart :chartData="stockData" :options="chartOptions" :label="product_Name" :key="recentEdits"></linechart>
    </div>
    <!-- The rest for the info card -->
    <div class="col-4" >
      <InfoCard v-on:data-update="dataUpdate" :InfoName="product_Name" :InfoID="product_ID" :_stockData="stockData" :key="recentEdits"></InfoCard>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import moment from "moment";
import Linechart from "./LineChart.vue";
import InfoCard from  "./InfoCard.vue";
export default {
  name: 'FlowDash',
  components: {
    Linechart,
    InfoCard
  },
  props: {
    p_id: String,
    p_name: String
  },
  data: function () {
    return {
      product_ID: this.p_id,
      product_Name: this.p_name,
      recentEdits: 0,
      stockData: [],
      // ChartJS options
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
          mode: "nearest"
        },
        scales:{
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: "Date"
            },
            type: 'time',
            ticks: {
                autoSkip: true,
                maxTicksLimit: 15
            }
          }],
          yAxes: [{
            scaleLabel: {
              display: true,
              labelString: "Inventory"
            },
          }],
        }, 
      },
    }
  },
  async mounted () {
    const _url = `http://localhost:5000/product/${this.product_ID}`;
    const {data} =  await axios.get(_url);
    const {stockRecord} = data;
    stockRecord.forEach(element => {
      const date = moment(element.date,"DD/MM/YYYY").format("YYYY-MM-DD");
      element.date = date;
    });
    this.stockData = stockRecord
  },
  methods: {
    // This function is to be called when a POST request 
    // has been made from the infocard to update the 'database'
    dataUpdate: 
      async function() {
        const _url = `http://localhost:5000/product/${this.product_ID}`;
        const {data} = await axios.get(_url);
        const {stockRecord} = data;
        stockRecord.forEach(element => {
          const date = moment(element.date,"DD/MM/YYYY").format("YYYY-MM-DD");
          element.date = date;
        });
        this.stockData = stockRecord
        this.recentEdits =+ 1;
      }

  }
}
</script>

