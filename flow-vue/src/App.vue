<template>
  <div class="container">
    <div>
      <div class="col-12 text-center">
        <h1>Flowlity Task</h1>
      </div>
    </div>
    <!-- The row below holds the dropdown buttons -->
    <div class="row" > 
      <div class="col-12">
        <!-- One for choosing a component by name -->
        <b-dropdown size="sm" id="dropdown-1" text="Component Name" class="m-md-2" v-model="selectedName">
          <b-dropdown-item v-for="product in productList" :key="product.id"  @click="clickName(product.name)">
            {{product.name}}
          </b-dropdown-item>
        </b-dropdown>
        <!-- One for choosing component by ID number -->
        <b-dropdown size="sm"  id="dropdown-2" text="Component ID" class="m-md-2">
          <b-dropdown-item v-for="product in productList" :key="product.id"  @click="clickID(product.id)">
            {{product.id}}
          </b-dropdown-item>
        </b-dropdown>
      </div>  
    </div>
    <!-- And then another row below holds our "Flowlity Dashboard" -->
    <div class="row">
      <div class="col-12">
        <!-- <flow-dash v-if="!selectedID"></flow-dash> -->
        <div v-if="!selectedID">
          <b-jumbotron header="Inventory Viewer" lead="Select a component by name or id">
          </b-jumbotron>
        </div>
        <FlowDash v-if="selectedID" :p_id="selectedID" :p_name="selectedName" :key="selectedID"></FlowDash>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import FlowDash from "./components/FlowDash.vue"
export default {
  name: 'App',
  components: {
    FlowDash
  },
  data() {
    return {
      selectedName: "",
      selectedID: "",
      idList: [],
      nameList: [],
      productList: [],
    };
  },
  async created() {
    // Get the available product information 
    const {data} = await axios.get("http://localhost:5000/");
    this.productList = data;
    data.forEach(d => {
      this.idList.push(d.id);
      this.nameList.push(d.name)
    });
  },
  methods: {
    // Handling dropdown selections
    // Just change the name if its different to the current one
    // And update the currently selected ID 
    clickName(_name) {
      if(this.selectedName === _name){
        return;
      }
      else {
        this.selectedName = _name;
        const _id = this.productList.find(o => o.name === this.selectedName).id;
        this.selectedID = _id;
      }
    },
    // Same as above, but just update ID
    clickID(_id) {
      if(this.selectedID === _id){
        return;
      }
      else {
        this.selectedID = _id;
      }
    },
  }
}
</script>

<style lang="scss" scoped>
  // .custom-dropdown {
  //   overflow-y:scroll;
  //   height:30vh;
  // }
</style>
