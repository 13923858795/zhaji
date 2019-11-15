<template>
  <div class="form">
    <div class="form-group">
      <label for="db_type">Database type</label>
      <select name="db_type" id="db_type" class="form-control" v-model="config.db_type">
        <option value>------------</option>
        <option value="oracle">Oracle</option>
      </select>
    </div>

    <div class="form-group">
      <label for="db_name">Database Name</label>
      <input type="text" class="form-control" id="db_name" v-model="config.db_name">
    </div>

    <div class="form-group">
      <label for="db_host">Database IP</label>
      <input type="text" class="form-control" id="db_host" v-model="config.db_host">
    </div>

    <div class="form-group">
      <label for="db_port">Database Port</label>
      <input type="text" class="form-control" id="db_port" v-model="config.db_port">
    </div>

    <div class="form-group">
      <label for="db_username">Database Username</label>
      <input type="text" class="form-control" id="db_username" v-model="config.db_username">
    </div>

    <div class="form-group">
      <label for="db_password">Database Password</label>
      <input type="text" class="form-control" id="db_password" v-model="config.db_password">
    </div>

    <hr>

    <button type="button" class="btn btn-success btn-quatek" @click.prevent.stop="submit()">OK</button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data: function() {
    return {
      config: {
        db_type: "",
        db_name: "",
        db_host: "",
        db_port: "",
        db_username: "",
        db_password: ""
      }
    };
  },
  methods: {
    submit() {
      console.log(this.config);
      axios
        .post("/update-other-database-config", this.config)
        .then(response => {
          console.log(response.data);
          alert("Save successfully!");
        })
        .catch(response => {
          console.log(response);
          alert("Save failed!");
        });
    },

    get_other_database_config() {
      axios
        .get("/get-other-database-config")
        .then(response => {
          console.log(response.data);
          this.config = response.data;
        })
        .catch(response => {
          console.log(response);
        });
    }
  },
  created() {
    this.get_other_database_config();
  }
};
</script>

<style scoped>
.btn-quatek {
  background-color: #059c66;
}
</style>
