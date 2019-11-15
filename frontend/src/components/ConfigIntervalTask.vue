<template>
  <div>
    <form class="form-inline">
      <label class="sr-only" for="task">Task</label>
      <select
        name="task"
        id="task"
        class="custom-select mb-2 mr-sm-2"
        v-model="interval_task.task"
      >
        <option value>------Task selection------</option>
        <option value="app.mod_task.tasks.send_email_of_logs:"
          >Task: Send all reports</option
        >
        <option value="app.mod_task.tasks.get_logs_from_mc_task"
          >Task:Get logs from gates</option
        >
        <option value="app.mod_task.tasks.save_to_other_database"
          >Task: Save to another</option
        >
        <option value="app.mod_task.tasks.update_cards_from_other_database"
          >Task: Card number synchronization</option
        >
      </select>

      <label class="sr-only" for="every"
        >Run every {{ interval_task.every }} seconds</label
      >
      <div class="input-group mb-2 mr-sm-2">
        <div class="input-group-prepend">
          <div class="input-group-text">Every </div>
        </div>
        <input
          type="text"
          class="form-control"
          id="every"
          v-model="interval_task.every"
          placeholder="Run every _ seconds"
        />
        <div class="input-group-append">
          <div class="input-group-text">Run every _ seconds</div>
        </div>
      </div>

      <button
        type="submit"
        class="btn btn-success mb-2 btn_quatek"
        @click.prevent.stop="submit()"
      >
        Add
      </button>
    </form>
    <br />
    <div>
      <div class="row">
        <table class="table table-striped table-responsive-md">
          <thead>
            <tr>
              <th scope="col">Task</th>
              <th scope="col">Running interval</th>
              <th scope="col">DELETE</th>
            </tr>
          </thead>

          <tbody v-if="!tasks.length">
            <tr>
              <td colspan="3" class="text-center">Task not found</td>
            </tr>
          </tbody>

          <tbody v-if="tasks.length">
            <tr v-for="task in computed_tasks" :key="task._id.$oid">
              <td>{{ task.task }}</td>
              <td>{{ task.interval.every }}</td>
              <td>
                <button
                  type="button"
                  class="btn btn-secondary btn-quatek btn-sm"
                  @click="delete_task(task._id.$oid)"
                >
                  <font-awesome-icon icon="trash-alt" />
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
import axios from 'axios'
import lodash from 'lodash'
export default {
  data: function() {
    return {
      tasks: [],
      interval_task: {
        task: '',
        every: '60'
      }
    }
  },
  computed: {
    computed_tasks() {
      let computed_tasks = lodash.cloneDeep(this.tasks)
      for (let task of computed_tasks) {
        if (task.task.indexOf('get_logs_from_mc_task') >= 0) {
          task.task = 'Get logs from gates'
        } else if (task.task.indexOf('send_email_of_logs') >= 0) {
          task.task = 'Send Report'
        } else if (task.task.indexOf('save_to_other_database') >= 0) {
          task.task = 'save to other database'
        }
      }
      return computed_tasks
    }
  },
  methods: {
    submit() {
      if (this.interval_task.task.length == 0) {
        return
      }
      axios
        .get(`/does-task-exist?q=${this.interval_task.task}`)
        .then(response => {
          console.log(response.data)
          if (response.data.does_task_exist === false) {
            axios
              .post('/task-interval-add-one', {
                every: this.interval_task.every,
                task: this.interval_task.task
              })
              .then(response => {
                console.log(response.data)
                this.get_tasks()
              })
              .catch(response => {
                console.log(response)
              })
          } else {
            alert('The current task already exists. Please do not add it again!')
          }
        })
        .catch(response => {
          console.log(response)
        })

      console.log(this.interval_task)
    },
    delete_task(task_id) {
      axios
        .post('/task-delete', { task_id: task_id })
        .then(response => {
          console.log(response.data)
          this.get_tasks()
        })
        .catch(response => {
          console.log(response)
        })
    },

    get_tasks() {
      axios
        .get('/task-interval')
        .then(response => {
          console.log(response)
          this.tasks = response.data
        })
        .catch(response => {
          console.log(response)
        })
    }
  },

  created() {
    this.get_tasks()
  }
}
</script>

<style scoped>
.btn_quatek {
  background-color: #059c66;
}
</style>


