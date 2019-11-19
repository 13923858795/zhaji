<template>
  <div>
    <div>
      <label>1. Card number conversion tool</label>
      <br>
      <small>Please put the HID card number in the first column of the excel file</small>
      <br>
      <br>
      <input type="file" name="hid_excel_file" id="hid_excel_file" ref="hid_excel_file">
      <button @click.prevent.stop="submit_hid_excel_file()">submit </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import fileDownload from "js-file-download";
export default {
  data() {
    return {
      //
    };
  },
  methods: {
    submit_hid_excel_file() {
      let formData = new FormData();
      let excel_file = this.$refs.hid_excel_file.files[0];
      formData.append("hid_excel_file", excel_file);
      axios
        .post("/hid_card_convertor", formData, {
          responseType: "blob",
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          console.log(response.data);
          fileDownload(
            response.data,
            "HID转换.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          );
        })
        .catch(response => {
          console.log(response);
        });
    }
  }
};
</script>

