<template>
  <div class="form">
    <div class="form-group">
      <label for="smtp_host">SMTP IP or Domain Name</label>
      <input type="text" class="form-control" id="smtp_host" v-model="config.smtp_host">
    </div>

    <div class="form-group">
      <label for="smtp_port">SMTP Port</label>
      <input type="text" class="form-control" id="smtp_port" v-model="config.smtp_port">
    </div>

    <div class="form-group form-check">
      <input
        type="checkbox"
        class="form-check-input"
        id="smtp_need_auth"
        v-model="config.smtp_need_auth"
      >
      <label class="form-check-label" for="smtp_need_auth">Need to verify</label>
    </div>

    <div class="form-group">
      <label for="smtp_username">The Usename of SMTP</label>
      <input type="text" class="form-control" id="smtp_username" v-model="config.smtp_username">
    </div>

    <div class="form-group" v-show="config.smtp_need_auth">
      <label for="smtp_password">The Password of SMTP</label>
      <input type="text" class="form-control" id="smtp_password" v-model="config.smtp_password">
    </div>

    <div class="form-group form-check">
      <input
        type="checkbox"
        class="form-check-input"
        id="smtp_use_ssl"
        v-model="config.smtp_use_ssl"
      >
      <label class="form-check-label" for="smtp_use_ssl">Use SSL</label>
    </div>
    <div class="form-group form-check">
      <input
        type="checkbox"
        class="form-check-input"
        id="smtp_use_tls"
        v-model="config.smtp_use_tls"
      >
      <label class="form-check-label" for="smtp_use_tls">Use TLS</label>
    </div>
    <hr>

    <div class="form-group">
      <label for="emalis">Email for Receiving Report</label>
      <input type="text" class="form-control" id="emalis" v-model="config.emails">
      <small id="emailsHelp" class="form-text text-muted">Format: a@example.com,b@example.com</small>
    </div>
    <hr>
    <div class="form-group">
      <label for="work_hours">Working time</label>
      <input type="text" class="form-control" id="work_hours" v-model="config.work_hours">
      <small id="work_hours_help" class="form-text text-muted">Format: 8:00-18:00</small>
    </div>

    <hr>
    <div class="form-group">
      <label for="timezone">Time Zone</label>
      <input type="text" class="form-control" id="timezone" v-model="config.timezone">
      <small id="timezone_help" class="form-text text-muted">example: +8</small>
    </div>

    <button type="button" class="btn btn-success btn-quatek" @click.prevent.stop="submit()">OK</button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data: function() {
    return {
      config: {
        smtp_host: "",
        smtp_port: "465",
        smtp_use_ssl: true,
        smtp_use_tls: true,
        smtp_username: "",
        smtp_password: "",
        emails: "",
        work_hours: "8:00-18:00",
        smtp_need_auth: true,
        timezone: ""
      }
    };
  },
  methods: {
    submit() {
      console.log(this.config);
      axios
        .post("/update-system-config", this.config)
        .then(response => {
          console.log(response.data);
          alert("Save successfully!");
        })
        .catch(response => {
          console.log(response);
          alert("Save failed!");
        });
    },
    get_system_config() {
      axios
        .get("/get-system-config")
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
    this.get_system_config();
  }
};
</script>

<style scoped>
.btn-quatek {
  background-color: #059c66;
}
</style>
