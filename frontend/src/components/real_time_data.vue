<template>
  <div class="container">
    <table class="table">
      <tr>
        <td>Log ID</td>
        <td>Card Number</td>
        <td>Name</td>
        <td>Job Number</td>
        <td>Card Category</td>
        <td>In/Out</td>
        <td>MC ID</td>
        <td>Time</td>
        <td>Pass or No</td>
        <td>Test or No</td>
        <td>Wrist Strap Data</td>
        <td>Left Shoes Data</td>
        <td>Right Shoes Data</td>
      </tr>
      <tr v-for="log in get_logs" :key="log.log_id">
        <td>{{log.log_id}}</td>
        <td>{{ log.card_number }}</td>
        <td>{{ log.name }}</td>
        <td>{{ log.job_number }}</td>
        <td>{{ log.card_category }}</td>
        <td>{{ log.in_out_symbol }}</td>
        <td>{{ log.mc_id }}</td>
        <td>{{ log.test_datetime | moment('YYYY-MM-DD HH:mm:ss') }}</td>
        <td>{{ log.test_result }}</td>
        <td>{{ log.is_tested }}</td>
        <td>{{ log.hand }}</td>
        <td>{{ log.left_foot }}</td>
        <td>{{ log.right_foot }}</td>
      </tr>
    </table>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      //
    };
  },
  computed: {
    ...mapGetters(["get_logs"])
  }
};
</script>
