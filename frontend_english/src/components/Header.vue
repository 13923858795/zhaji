<template>
  <b-navbar toggleable="md" type="dark" variant="dark">
    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

    <b-navbar-brand href="#">
      <img @click="toIndex()" src="@/assets/logo.png" alt="Quatek">
    </b-navbar-brand>

    <b-collapse is-nav id="nav_collapse">
      <b-navbar-nav>
        <b-nav-item :to="{name: 'Index'}" exact>Home Page</b-nav-item>
        <b-nav-item :to="{name: 'Gates'}" v-if="is_authenticated">Gate List</b-nav-item>
        <b-nav-item :to="{name: 'Cards'}" v-if="is_authenticated">Card Management</b-nav-item>
        <b-nav-item :to="{name: 'CardTests'}">ESD Test</b-nav-item>
        <b-nav-item :to="{name: 'real_time_data'}">Real-time Data</b-nav-item>
        <!-- <b-nav-item :to="{name: 'Attendances'}">考勤管理</b-nav-item> -->
        <!-- <b-nav-item :to="{name: 'Analysis'}" v-if="is_authenticated">数据统计</b-nav-item> -->
        <b-nav-item :to="{name: 'Config'}" v-if="is_authenticated">Setting</b-nav-item>
        <!-- <b-nav-item href="#">Help</b-nav-item> -->
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <!-- <b-nav-form>
            <b-form-input size="sm" class="mr-sm-2" type="text" placeholder="Search" />
            <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
        </b-nav-form>-->
        <!-- <b-nav-item-dropdown text="Lang" right>
            <b-dropdown-item href="#">EN</b-dropdown-item>
            <b-dropdown-item href="#">ES</b-dropdown-item>
            <b-dropdown-item href="#">RU</b-dropdown-item>
            <b-dropdown-item href="#">FA</b-dropdown-item>
        </b-nav-item-dropdown>-->
        <b-nav-item-dropdown right>
          <!-- Using button-content slot -->
          <template slot="button-content">
            <em>My</em>
          </template>
          <!-- <b-dropdown-item href="#">Profile</b-dropdown-item> -->
          <b-dropdown-item :to="{name: 'login'}" v-if="!is_authenticated">Login</b-dropdown-item>
          <b-dropdown-item @click.stop.prevent="logout()" v-if="is_authenticated">Log out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
export default {
  data() {
    return {};
  },
  computed: {
    ...mapGetters(["is_authenticated"])
  },
  methods: {
    toIndex() {
      this.$router.push({ name: "Index" });
    },

    ...mapActions(["logout"])
  }
};
</script>




<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
/*  Small devices (landscape phones, 576px and up) */
.navbar {
  margin-bottom: 20px;
}
@media (min-width: 576px) {
}

/*  Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
}

/*  Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
}

/*  Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
}
</style>
