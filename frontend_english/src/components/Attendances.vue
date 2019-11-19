<template>
  <div class="container">
    <div class="form-row search-row">
      <div class="input-group">
        <datetime
          v-model="date3"
          type="datetime"
          input-class="form-control"
          format="yyyy-MM-dd HH:mm"
          :phrases="{ok: 'OK', cancel: 'CANCEL'}"
          :minute-step="10"
        ></datetime>

        <label class="col-sm-1 text-center search-space">至</label>
        <datetime
          v-model="date3"
          type="datetime"
          input-class="form-control"
          format="yyyy-MM-dd HH:mm"
          :phrases="{ok: 'OK', cancel: 'CANCEL'}"
          :minute-step="10"
        ></datetime>
        <label class="col-sm-4 text-center search-space"></label>
        <select class="form-control col-sm-3">
          <option value>All States</option>
          <option value>States1</option>
          <option value>States2</option>
          <option value>States3</option>
          <option value>States4</option>
        </select>
      </div>
      <div class="w-100">
        <br>
      </div>
      <div class="input-group">
        <input
          type="text"
          class="form-control"
          aria-label="Search string"
          aria-describedby="basic-addon2"
        >
        <div class="input-group-append">
          <button class="btn btn-outline-success btn-outline-quatek" type="button">
            <font-awesome-icon icon="search"/>Search
          </button>
        </div>
      </div>
    </div>
    <div class="row btn-row">
      <p class="w-100 text-right">
        <button type="button" class="btn btn-secondary btn-row-btn btn-sm" title="email Send test">
          <font-awesome-icon icon="envelope"/>
        </button>
      </p>
    </div>
    <div class="row">
      <table class="table table-striped table-responsive-md">
        <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Job number</th>
            <th scope="col">Card number</th>
            <th scope="col">Card type</th>
            <th scope="col">Department</th>
            <th scope="col">Modify</th>
            <th scope="col">Delete</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="card in 25" :key="card">
            <td>Name</td>
            <td>12938475</td>
            <td>384758692747387</td>
            <td>Card type 1</td>
            <td>Department 1</td>
            <td>
              <button type="button" class="btn btn-secondary btn-quatek btn-sm">
                <font-awesome-icon icon="pencil-alt"/>
              </button>
            </td>
            <td>
              <button type="button" class="btn btn-secondary btn-quatek btn-sm">
                <font-awesome-icon icon="trash-alt"/>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <nav aria-label="Page navigation">
      <ul class="pagination justify-content-center">
        <li class="page-item">
          <a class="page-link" href="#" aria-label="Previous">
            <span aria-hidden="true">
              <font-awesome-icon icon="caret-square-left"/>
            </span>
            <span class="sr-only">Previous page</span>
          </a>
        </li>
        <li class="page-item disabled">
          <a class="page-link">this {{currentPage}} page</a>
        </li>

        <li class="page-item">
          <a class="page-link" href="#" aria-label="Next">
            <span aria-hidden="true">
              <font-awesome-icon icon="caret-square-right"/>
            </span>
            <span class="sr-only">next page</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  name: "Attendances",
  data: function() {
    return {
      currentPage: 1,
      date1: this.$moment().format("YYYY-MM-DDTHH:mm:ss"),
      date2: this.$moment().format("YYYY-MM-DDTHH:mm:ss"),
      date3: this.$moment().format("YYYY-MM-DDTHH:mm:ss")
    };
  },
  props: {},
  components: {}
};
</script>



<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
/*  Small devices (landscape phones, 576px and up) */
.search-row {
  margin: 0 0 20px 0;
}
.search-space {
  padding-top: 5px;
}
.btn-outline-quatek {
  color: #059c66;
  border-color: #059c66;
}

.btn-row-btn {
  margin: 0 5px;
  background-color: #868686;
}
.btn-quatek {
  background-color: #868686;
}

.page-link {
  color: #059c66;
}
.vdatetime {
  width: 100%;
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
  .search-row {
    margin: 0 -15px 20px -15px;
  }
  .vdatetime {
    width: 20%;
  }
}
</style>