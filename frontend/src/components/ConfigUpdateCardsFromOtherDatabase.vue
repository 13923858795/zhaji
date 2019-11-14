<template>
  <div class="form">
    <div class="form-group">
      <label for="update_db_type">Database type</label>
      <select
        name="update_db_type"
        id="update_db_type"
        class="form-control"
        v-model="config.update_db_type"
      >
        <option value>------------</option>
        <option value="oracle">Oracle</option>
      </select>
    </div>

    <div class="form-group">
      <label for="update_db_name">Database name/Example/SID</label>
      <input
        type="text"
        class="form-control"
        id="update_db_name"
        v-model="config.update_db_name"
      />
    </div>

    <div class="form-group">
      <label for="update_db_host">Database IP</label>
      <input
        type="text"
        class="form-control"
        id="update_db_host"
        v-model="config.update_db_host"
      />
    </div>

    <div class="form-group">
      <label for="update_db_port">Database port</label>
      <input
        type="text"
        class="form-control"
        id="update_db_port"
        v-model="config.update_db_port"
      />
    </div>

    <div class="form-group">
      <label for="update_db_username">Database username</label>
      <input
        type="text"
        class="form-control"
        id="update_db_username"
        v-model="config.update_db_username"
      />
    </div>

    <div class="form-group">
      <label for="update_db_password">Database password</label>
      <input
        type="text"
        class="form-control"
        id="update_db_password"
        v-model="config.update_db_password"
      />
    </div>

    <div class="form-group">
      <label for="update_db_table_name">Database Table</label>
      <input
        type="text"
        class="form-control"
        id="update_db_table_name"
        v-model="config.update_db_table_name"
      />
    </div>

    <hr />

    <button
      type="button"
      class="btn btn-success btn-quatek"
      @click.prevent.stop="submit()"
    >
      OK
    </button>

    <button
      type="button"
      class="btn btn-success btn-quatek"
      @click.prevent.stop="sync()"
    >
      Manual synchronization
    </button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data: function() {
    return {
      config: {
        update_db_type: '',
        update_db_name: '',
        update_db_host: '',
        update_db_port: '',
        update_db_username: '',
        update_db_password: '',
        update_db_table_name: ''
      }
    }
  },
  methods: {
    submit() {
      console.log(this.config)
      axios
        .post('/update-update-database-config', this.config)
        .then(response => {
          console.log(response.data)
          alert('Save successfully!')
        })
        .catch(response => {
          console.log(response)
          alert('Save failed!')
        })
    },
    sync() {
      axios
        .post('/manual-update-database')
        .then(response => {
          console.log(response.data)
          alert('Receive synchronization instruction!')
        })
        .catch(response => {
          console.log(response)
          alert('Synchronization instruction failed!')
        })
    },

    get_update_database_config() {
      axios
        .get('/get-update-database-config')
        .then(response => {
          console.log(response.data)
          this.config.update_db_type = response.data.update_db_type
            ? response.data.update_db_type
            : ''
          this.config.update_db_name = response.data.update_db_name
            ? response.data.update_db_name
            : ''
          this.config.update_db_host = response.data.update_db_host
            ? response.data.update_db_host
            : ''
          this.config.update_db_port = response.data.update_db_port
            ? response.data.update_db_port
            : ''
          this.config.update_db_username = response.data.update_db_username
            ? response.data.update_db_username
            : ''
          this.config.update_db_password = response.data.update_db_password
            ? response.data.update_db_password
            : ''
          this.config.update_db_table_name = response.data.update_db_table_name
            ? response.data.update_db_table_name
            : ''
        })
        .catch(response => {
          console.log(response)
        })
    }
  },
  created() {
    this.get_update_database_config()
  }
}
</script>

<style scoped>
.btn-quatek {
  background-color: #059c66;
}
</style>
