<template>
  <div class="container-fluid">
    <div class="row">
      <b-nav vertical class="col-md-2 offset-md-1 sidebar">
        <b-nav-item :to="{ name: 'system-config' }" key="system-config"
          >Email and SMTP</b-nav-item
        >
        <b-nav-item :to="{ name: 'other-database' }" key="other-database"
          >Database connection</b-nav-item
        >
        <b-nav-item :to="{ name: 'interval-task' }" key="interval-task"
          >Task design(According to the interval)</b-nav-item
        >
        <b-nav-item :to="{ name: 'crontab-task' }" key="crontab-task"
          >Task design(According to the time)</b-nav-item
        >
        <b-nav-item :to="{ name: 'background-task' }" key="background-task"
          >Administrator tools</b-nav-item
        >
        <b-nav-item :to="{ name: 'class-time-config' }" key="class-time-config"
          >Class Setting</b-nav-item
        >
        <b-nav-item
          :to="{ name: 'card_number_convertor_config' }"
          key="card_number_convertor_config"
          >Card number conversion tool</b-nav-item
        >
        <b-nav-item
          :to="{ name: 'update-cards-from-other-database' }"
          key="update-cards-from-other-database"
          >Card number synchronization</b-nav-item
        >
        <br />
      </b-nav>

      <div class="col-md-9">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {}
}
</script>

<style scoped>
.container-fluid {
  min-height: 500px;
}
.sidebar a {
  color: #059c66;
}
.sidebar a.active {
  /* color: white; */
  background-color: #e9ecef;
}
</style>
