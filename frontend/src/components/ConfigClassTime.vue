<template>
  <div>
    <form class="form-inline">
      <label class="sr-only" for="class_time_name">Class name</label>
      <div class="input-group mb-2 mr-sm-2">
        <input
          type="text"
          class="form-control"
          id="class_time_name"
          v-model="class_time_name"
          placeholder="Class name"
        >
      </div>

      <label class="sr-only" for="class_time_from">The star time of the class</label>
      <div class="input-group mb-2 mr-sm-2">
        <input
          type="text"
          class="form-control"
          id="class_time_from"
          v-model="class_time_from"
          placeholder="The star time of the class"
        >
      </div>

      <label class="sr-only" for="class_time_to">The end time of the class</label>
      <div class="input-group mb-2 mr-sm-2">
        <input
          type="text"
          class="form-control"
          id="class_time_to"
          v-model="class_time_to"
          placeholder="The end time of the class"
        >
      </div>

      <button
        type="submit"
        class="btn btn-success mb-2 btn_quatek"
        @click.prevent.stop="submit()"
      >添加</button>
    </form>
    <br>
    <div>
      <div class="row">
        <table class="table table-striped table-responsive-md">
          <thead>
            <tr>
              <th scope="col">Class name</th>
              <th scope="col">Start time</th>
              <th scope="col">End time</th>
              <th scope="col">Delete</th>
            </tr>
          </thead>

          <tbody v-if="!class_times.length">
            <tr>
              <td colspan="4" class="text-center">No class found</td>
            </tr>
          </tbody>

          <tbody v-if="class_times.length">
            <tr v-for="class_time in class_times" :key="class_time._id.$oid">
              <td>{{class_time.name}}</td>
              <td>{{class_time.working_time_from}}</td>
              <td>{{class_time.working_time_to}}</td>
              <td>
                <button
                  type="button"
                  class="btn btn-secondary btn-quatek btn-sm"
                  @click="delete_class_time(class_time._id.$oid)"
                >
                  <font-awesome-icon icon="trash-alt"/>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
// import lodash from 'lodash';
export default {
  data: function() {
    return {
      class_times: [],
      class_time_name: "",
      class_time_from: "",
      class_time_to: ""
    };
  },
  computed: {},
  methods: {
    submit() {
      if (this.class_time_name.length == 0) {
        return;
      }
      axios
        .post(`/add-class-time`, {
          class_time_name: this.class_time_name,
          class_time_from: this.class_time_from,
          class_time_to: this.class_time_to
        })
        .then(response => {
          console.log(response.data);
          this.class_time_name = "";
          this.class_time_from = "";
          this.class_time_to = "";
          this.get_class_times();
        })
        .catch(response => {
          console.log(response);
        });

      console.log(this.interval_task);
    },

    delete_class_time(class_time_id) {
      axios
        .post("/delete-class-time", { class_time_id: class_time_id })
        .then(response => {
          console.log(response.data);
          this.get_class_times();
        })
        .catch(response => {
          console.log(response);
        });
    },

    get_class_times() {
      axios
        .get("/get-class-times")
        .then(response => {
          console.log(response);
          this.class_times = response.data;
        })
        .catch(response => {
          console.log(response);
        });
    }
  },

  created() {
    this.get_class_times();
  }
};
</script>

<style scoped>
.btn_quatek {
  background-color: #059c66;
}
</style>


