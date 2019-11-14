<template>
  <div class="container">
    <form class="card-create-form">
      <div class="form-group row">
        <label for="cardNumber" class="col-sm-2 col-form-label">Card number *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="cardNumber" v-model="card.card_number">
        </div>
      </div>

      <div class="form-group row">
        <label for="hid_number" class="col-sm-2 col-form-label">HID card number *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="hid_number" v-model="card.hid_number">
        </div>
      </div>

      <div class="form-group row">
        <label for="card_category" class="col-sm-2 col-form-label">Card category *</label>
        <div class="col-sm-10">
          <select class="form-control" id="card_category" v-model="card.card_category">
            <option value="0">VIP</option>
            <option value="1">只测手</option>
            <option value="2">只测脚</option>
            <option value="3">手脚都测</option>
          </select>
        </div>
      </div>

      <div class="form-group row">
        <label for="name" class="col-sm-2 col-form-label">Name *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="name" v-model="card.name">
        </div>
      </div>

      <div class="form-group row">
        <label for="job_number" class="col-sm-2 col-form-label">Job number *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="job_number" v-model="card.job_number">
        </div>
      </div>

      <div class="form-group row">
        <label for="department" class="col-sm-2 col-form-label">Department *</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="department" v-model="card.department">
        </div>
      </div>

      <div class="form-group row">
        <label for="gender" class="col-sm-2 col-form-label">Gender *</label>
        <div class="col-sm-10">
          <select class="form-control" id="gender" v-model="card.gender">
            <option value="0">女</option>
            <option value="1">男</option>
          </select>
        </div>
      </div>

      <div class="form-group row">
        <label for="classes" class="col-sm-2 col-form-label">Class</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="classes" v-model="card.classes">
        </div>
      </div>

      <div class="form-group row">
        <label for="note" class="col-sm-2 col-form-label">Note</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="note" v-model="card.note">
        </div>
      </div>

      <div class="form-group row">
        <label for="belong_to_mc" class="col-sm-2 col-form-label">Gate permission</label>
        <div class="col-sm-10">
          <input
            type="text"
            class="form-control"
            id="belong_to_mc"
            v-model="card.belong_to_mc"
            @focus="show_modal=true"
            readonly
          >
          <small
            class="form-text text-muted"
          >format: "gate_1:0|gate_2:1|gate_3:3"; 0：Allow access,1: No entry/exit allowed,2: No exit/entry allowed,3: Banned in and out. </small>
        </div>
      </div>

      <div class="form-group row text-center">
        <div class="col-sm-12">
          <button
            type="submit"
            class="btn btn-success btn-block submit-btn"
            @click.prevent="submit()"
            :disabled="submit_is_disabled"
          >OK</button>
        </div>
      </div>
    </form>

    <b-modal
      v-model="show_modal"
      title="Gate permission"
      ok-only
      ok-title="OK"
      :lazy="true"
      @ok="confirm()"
      ok-variant="success"
    >
      <b-container fluid class="form-inline">
        <b-row v-for="(gate,index) in computed_rights" :key="gate.gate_name" class="w-100">
          <label :for="'gate_'+index" class="col-6">{{index+1}} - Gate name: {{gate.gate_name}}</label>
          <select :id=" 'gate_'+index" class="form-control col-6" v-model="gate.rights">
            <option value="0">Allow access</option>
            <option value="1">No entry/exit allowed</option>
            <option value="2">No exit/entry allowed</option>
            <option value="3">Banned in and out</option>
          </select>
          <hr class="w-100">
        </b-row>
      </b-container>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "",
  data() {
    return {
      card: {
        id: "",
        card_number: "",
        card_category: "",
        name: "",
        job_number: "",
        department: "",
        gender: "",
        note: "",
        belong_to_mc: "",
        classes: "",
        hid_number: ""
      },
      submit_is_disabled: false,
      show_modal: false,
      gates: []
    };
  },
  computed: {
    computed_rights() {
      let computed_rights = [];
      if (this.card.id) {
        for (let gate_right of this.card.belong_to_mc.split("|")) {
          if (!gate_right) {
            computed_rights.push({
              gate_name: gate_right.split(":")[0],
              rights: gate_right.split(":")[1]
            });
          }
        }
      }
      for (let gate of this.gates) {
        if (
          computed_rights.filter(obj => obj.gate_name === gate.name).length ===
          0
        ) {
          computed_rights.push({ gate_name: gate.name, rights: "0" });
        }
      }
      return computed_rights;
    }
  },
  methods: {
    submit() {
      this.submit_is_disabled = true;
      console.log(this.card);
      if (
        this.card.card_category &&
        this.card.name &&
        this.card.job_number &&
        this.card.department &&
        this.card.gender
      ) {
        if (this.card.hid_number === "undefined") {
          this.card.hid_number = "";
        }

        if (this.card.id) {
          axios
            .patch("/cards/create", this.card)
            .then(response => {
              console.log(response);
              alert("保存成功!");
              this.$router.push({ name: "Cards" });
            })
            .catch(response => {
              console.log(response);
              alert("保存失败!");
              this.submit_is_disabled = false;
            });
        } else {
          axios
            .post("/cards/create", this.card)
            .then(response => {
              console.log(response);
              alert("保存成功!");
              this.$router.push({ name: "Cards" });
            })
            .catch(response => {
              console.log(response);
              alert("保存失败!");
              this.submit_is_disabled = false;
            });
        }
      } else {
        alert("带*的信息不能为空!");
        this.submit_is_disabled = false;
      }
    },
    confirm() {
      let rights = [];
      for (let gate_rights of this.computed_rights) {
        rights.push(gate_rights.gate_name + ":" + gate_rights.rights);
      }
      console.log(rights);

      this.card.belong_to_mc = rights.join("|");
    }
  },
  created() {
    if (this.$route.params.card_id) {
      this.card.id = this.$route.params.card_id;
      axios
        .get(`/get-card-by-id?q=${this.card.id}`)
        .then(response => {
          console.log("card: ", response.data);
          this.card.card_number = response.data[0].card_number;
          this.card.card_category = response.data[0].card_category;
          this.card.name = response.data[0].name;
          this.card.job_number = response.data[0].job_number;
          this.card.department = response.data[0].department;
          this.card.gender = response.data[0].gender;
          this.card.note = response.data[0].note;
          this.card.belong_to_mc = response.data[0].belong_to_mc;
          this.card.number_in_mc = response.data[0].number_in_mc;
          this.card.classes = String(response.data[0].classes);
          this.card.hid_number = String(response.data[0].hid_card_number);
          console.log(this.card);
        })
        .catch(response => {
          console.log(response);
        });
    }

    axios
      .get(`/gates?offset=0&limit=10000`)
      .then(response => {
        console.log(response);
        this.gates = response.data;
        this.currentPage = 1;
      })
      .catch(response => {
        console.log(response);
      });
  }
};
</script>


<style scoped>
/* Extra small devices (portrait phones, less than 576px)
 No media query for `xs` since this is the default in Bootstrap */
/*  Small devices (landscape phones, 576px and up) */
.submit-btn {
  color: #ffffff;
  background-color: #059c66;
}
.vdatetime-popup__header {
  background-color: #059c66;
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
  .card-create-form {
    margin-top: 60px;
  }
  .submit-btn {
    margin-top: 30px;
  }
}
</style>