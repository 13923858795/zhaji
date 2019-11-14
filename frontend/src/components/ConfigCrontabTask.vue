<template>
  <div>
    <form class="form-inline">
      <label class="sr-only" for="task">Task</label>
      <select name="task" id="task" class="custom-select mb-2 mr-sm-2" v-model="crontab_task.task">
        <option value>------Task selection------</option>
        <option value="app.mod_task.tasks.send_email_of_logs:">Task: Send all reports</option>
        <option value="app.mod_task.tasks.get_logs_from_mc_task">Task:Get logs from gates</option>
        <option value="app.mod_task.tasks.save_to_other_database">Task: Save to another </option>
        <option
          v-for="card_class in card_classes"
          :value="'app.mod_task.tasks.send_email_of_logs:'+card_class.name"
          :key="card_class.name"
        >task: send{{card_class.name}}class report </option>
      </select>

      <label class="sr-only" for="minute">Minute</label>
      <div class="input-group mb-2 mr-sm-2">
        <input
          type="text"
          class="form-control"
          id="minute"
          v-model="crontab_task.minute"
          placeholder="0 - 59"
        >
        <div class="input-group-append">
          <div class="input-group-text">Minute</div>
        </div>
      </div>

      <label class="sr-only" for="hour">Hour</label>
      <div class="input-group mb-2 mr-sm-2">
        <input
          type="text"
          class="form-control"
          id="hour"
          v-model="crontab_task.hour"
          placeholder="0 - 23"
        >
        <div class="input-group-append">
          <div class="input-group-text">Hour</div>
        </div>
      </div>

      <label class="sr-only" for="day_of_month">Day</label>
      <div class="input-group mb-2 mr-sm-2">
        <input
          type="text"
          class="form-control"
          id="day_of_month"
          v-model="crontab_task.day_of_month"
          placeholder="1 - 31"
        >
        <div class="input-group-append">
          <div class="input-group-text">Day</div>
        </div>
      </div>

      <label class="sr-only" for="month_of_year">Week</label>
      <select
        name="task"
        id="month_of_year"
        class="custom-select mb-2 mr-sm-2"
        v-model="crontab_task.month_of_year"
      >
        <option value="*">All mounth</option>
        <option value="1">January </option>
        <option value="2">February </option>
        <option value="3">March </option>
        <option value="4">April </option>
        <option value="5">May </option>
        <option value="6">June </option>
        <option value="7">July </option>
        <option value="8">August </option>
        <option value="9">September </option>
        <option value="10">October </option>
        <option value="11">November </option>
        <option value="12">December</option>
      </select>

      <label class="sr-only" for="day_of_week">月</label>
      <select
        name="task"
        id="day_of_week"
        class="custom-select mb-2 mr-sm-2"
        v-model="crontab_task.day_of_week"
      >
        <option value="*">All day</option>
        <option value="0">Sunday</option>
        <option value="1">Monday</option>
        <option value="2">Tuesday</option>
        <option value="3">Wednesday</option>
        <option value="4">Thursday</option>
        <option value="5">Friday</option>
        <option value="6">Saturday</option>
      </select>

      <button
        type="submit"
        class="btn btn-success mb-2 btn_quatek"
        @click.prevent.stop="submit()"
      >add</button>
    </form>
    <small id="passwordHelpBlock" class="form-text text-muted">
      Learn more:
      <a href="https://zh.wikipedia.org/wiki/Cron" target="_blank">crontab wikipedia</a>
      <span>&#160;</span>
      大陆用户请使用:
      <a
        href="https://baike.baidu.com/item/crontab/8819388"
        target="_blank"
      >crontab Baidu Encyclopedia</a>
    </small>
    <br>
    <div>
      <div class="row">
        <table class="table table-striped table-responsive-md">
          <thead>
            <tr>
              <th scope="col">Task</th>
              <th scope="col">Running time(min\hour\day\month\week)</th>
              <th scope="col">Delete</th>
            </tr>
          </thead>

          <tbody v-if="!tasks.length">
            <tr>
              <td colspan="3" class="text-center">Task not found</td>
            </tr>
          </tbody>

          <tbody v-if="tasks.length">
            <tr v-for="task in computed_tasks" :key="task._id.$oid">
              <td>
                {{task.task}}
                <span v-if="task.args[0]!== ''">: {{task.args[0]}} Class</span>
              </td>
              <td>{{task.crontab.minute}} | {{task.crontab.hour}} | {{task.crontab.day_of_month}} | {{task.crontab.month_of_year}} | {{task.crontab.day_of_week}}</td>
              <td>
                <button
                  type=" button"
                  class="btn btn-secondary btn-quatek btn-sm"
                  @click="delete_task(task._id.$oid)"
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
import lodash from "lodash";
export default {
  data() {
    return {
      tasks: [],
      crontab_task: {
        task: "",
        minute: "*",
        hour: "*",
        day_of_month: "*",
        month_of_year: "*",
        day_of_week: "*"
      },
      card_classes: []
    };
  },

  computed: {
    computed_tasks() {
      let computed_tasks = lodash.cloneDeep(this.tasks);
      for (let task of computed_tasks) {
        if (task.task.indexOf("get_logs_from_mc_task") >= 0) {
          task.task = "Get logs from gates";
        } else if (task.task.indexOf("send_email_of_logs") >= 0) {
          task.task = "Send all reports";
        } else if (task.task.indexOf("save_to_other_database") >= 0) {
          task.task = "Save to another";
        }

        if (task.crontab.hour !== "*") {
          let hour =
            Number(task.crontab.hour) - new Date().getTimezoneOffset() / 60;
          if (hour >= 24) {
            task.crontab.hour = hour - 24;
          } else {
            task.crontab.hour = hour;
          }
        }
      }
      return computed_tasks;
    }
  },

  methods: {
    submit() {
      if (this.crontab_task.task.length == 0) {
        return;
      }
      if (
        !(
          this.crontab_task.minute === "*" ||
          (Number(this.crontab_task.minute) <= 59 &&
            Number(this.crontab_task.minute) >= 0)
        )
      ) {
        alert("minute Configure error!");
        return;
      }
      if (
        !(
          this.crontab_task.hour === "*" ||
          (Number(this.crontab_task.hour) <= 23 &&
            Number(this.crontab_task.hour) >= 0)
        )
      ) {
        alert("hou Configure error!");
        return;
      }
      if (
        !(
          this.crontab_task.day_of_month === "*" ||
          (Number(this.crontab_task.day_of_month) <= 31 &&
            Number(this.crontab_task.day_of_month) >= 1)
        )
      ) {
        alert("day Configure error!");
        return;
      }
      axios
        .get(`/does-task-exist?q=${this.crontab_task.task}`)
        .then(response => {
          console.log(response.data);
          if (response.data.does_task_exist === false) {
            axios
              .post("/task-crontab-add-one", {
                task: this.crontab_task.task,
                minute: this.crontab_task.minute,
                hour: this.computed_hour(this.crontab_task.hour),
                day_of_month: this.crontab_task.day_of_month,
                month_of_year: this.crontab_task.month_of_year,
                day_of_week: this.crontab_task.day_of_week
              })
              .then(response => {
                console.log(response.data);
                this.get_tasks();
              })
              .catch(response => {
                console.log(response);
              });
          } else {
            alert("The current task already exists. Please do not add it again!");
          }
        })
        .catch(response => {
          console.log(response.data);
        });

      console.log(this.crontab_task);
    },

    delete_task(task_id) {
      axios
        .post("/task-delete", { task_id: task_id })
        .then(response => {
          console.log(response.data);
          this.get_tasks();
        })
        .catch(response => {
          console.log(response);
        });
    },

    get_tasks() {
      axios
        .get("/task-crontab")
        .then(response => {
          console.log(response);
          this.tasks = response.data;
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
          this.card_classes = response.data;
        })
        .catch(response => {
          console.log(response);
        });
    },

    computed_hour(hour) {
      if (hour === "*") {
        return "*";
      } else {
        let hour2 = Number(hour) + new Date().getTimezoneOffset() / 60;
        if (hour2 >= 0) {
          return String(hour2);
        } else {
          return String(hour2 + 24);
        }
      }
    }
  },

  created() {
    this.get_tasks();
    this.get_class_times();
  }
};
</script>


<style scoped>
.btn_quatek {
  background-color: #059c66;
}
</style>