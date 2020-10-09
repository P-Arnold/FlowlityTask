<script>
import {Line} from 'vue-chartjs';

export default {
    extends: Line,
    props: {
        label: {
            type: String
        },
        chartData: {
            type: Array
        },
        options: {
            type: Object
        }
    },
    mounted() {
        const dates = this.chartData.map(d => d.date);
        const stock = this.chartData.map(d=>d.stock);
        this.renderChart( {
            labels: dates,
            datasets: [
                {
                label: this.label,
                data: stock,
                radius: 1,
                hitRadius: 8,
                hoverRadius: 5,
                borderColor: "rgba(40,242,155,0.5)",
                pointBackgroundColor: "rgba(40,242,155,0.9)",
                backgroundColor: "rgba(0,0,0,0)"
                }
            ],
        },
        this.options);
    },
    beforeUpdate: function() {
        console.log("pre")
    }
    
}
</script>