<template>
    <b-card style="height:100%">
        <template v-slot:header>
            <h4 class="mb-0">Component Info</h4>
        </template>
        <b-card-body>
            <h6 class="card-subtitle mb-2 "><strong>Name:</strong> {{productName}} </h6>
            <h6 class="card-subtitle mb-2 "><strong>ID:</strong> {{productID}}</h6>
            <h6 class="card-subtitle mb-2 "><strong>Inventory</strong> on <strong>{{currentDate}}:</strong> {{currentStock}}</h6>
        </b-card-body> 
        <b-button variant="outline-secondary" @click="editing=!editing">Edit</b-button>
        <div v-if="editing">
            <b-form-datepicker 
            id="example-datepicker" v-model="editDate"
            :min="earliestDate" :max="currentDate"
            @context="datefun" class="mb-2">
            </b-form-datepicker>
            <p>Date: {{ editDate }}</p>
            <p>Stock: <input v-model="editStock" placeholder="Enter new stock"></p>
            <b-button variant="primary" @click="submit">Submit</b-button>
        </div>
    </b-card>
</template>

<script>
import axios from "axios";
export default {
    name: "InfoCard",
    props: {
        InfoName: String,
        InfoID: String,
        _stockData: Array
    },
    data() {
        return {
            productName: this.InfoName,
            productID: this.InfoID,
            currentStock: null, 
            currentDate: null,
            earliestDate: null,
            editing: false,
            editDate: "",
            editStock: null,
            stockData: this._stockData,
        }
    },
    mounted: function () {
        const datesArray = this._stockData.map(d => d.date);
        const inventoryArray = this._stockData.map(d=>d.stock);
        this.currentDate = datesArray[datesArray.length-1];
        this.earliestDate = datesArray[0];
        this.currentStock = inventoryArray[inventoryArray.length-1];
        this.editDate =  this.currentDate;
        this.editStock = this.currentStock;
    },
    updated: function () {
    },
    methods: {
        datefun() {
            const newStock = this.stockData.find(p=>p.date==this.editDate).stock;
            this.editStock = newStock;
        },
        submit() {
            if(this.editStock>=0){
                axios.post(`http://localhost:5000/update/${this.productID}/${this.editDate}/${this.editStock}`).then(
                    (promise) => {
                        const {data} = promise
                        if (data.success) {
                            this.$emit("data-update")
                            const inventoryArray = this._stockData.map(d=>d.stock);
                            this.currentStock = inventoryArray[inventoryArray.length-1];
                        }
                    }
                )
            }
        }
    }
    
}
</script>