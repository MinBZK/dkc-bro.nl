<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="table_data"
      :items-per-page="5"
      class="elevation-1"
    >
      <template v-slot:item.percentageFailed="{ item }">
        <span>{{ item.percentageFailed.toFixed(2) + "%" }}</span>
      </template>
      <template v-slot:item.trend="{ item }">
        <div class="trend__cell">
          <img
            style="height: 16px"
            :style="{
              transform: 'rotate(-' + getTrendRotation(item.trend) + 'deg)',
            }"
            :class="get_color_filter(item.trend)"
            src="@/assets/icon-arrow.svg"
            alt=""
          />&nbsp;
          <span>{{
            (item.trend >= 0 ? "+" : "") + item.trend.toFixed(2)
          }}</span>
        </div>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
export default {
  data() {
    return {
      headers: [
        {
          text: "Bron",
          align: "start",
          sortable: false,
          value: "source",
        },
        { text: "Peildatum", value: "date" },
        { text: "Trend", value: "trend" },
        { text: "Regels", value: "nrActiveRules" },
        { text: "Records", value: "nrRecords" },
        { text: "Afgekeurd", value: "nrFailedRecords" },
        { text: "Afgekeurd (%)", value: "percentageFailed" },
      ],
      table_data: [],
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    getData() {
      axios({
        url: `${this.$store.state.APIurl}/batch/statistics`,
        method: "GET",
      })
        .then((response) => {
          this.table_data = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getTrendRotation(trend) {
      const intensity = 25;
      return Math.max(Math.min(trend * intensity + 90, 180), 0);
    },
    get_color_filter(trend) {
      const treshold = 0.3;
      if (trend > treshold) {
        return "green_filter";
      } else if (trend < -treshold) {
        return "red_filter";
      } else {
        return "blue_filter";
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.trend__cell {
  align-items: center !important;
  display: flex;
}

.green_filter {
  filter: invert(58%) sepia(77%) saturate(6055%) hue-rotate(128deg)
    brightness(101%) contrast(101%);
}
.red_filter {
  filter: invert(13%) sepia(97%) saturate(6829%) hue-rotate(1deg)
    brightness(107%) contrast(110%);
}
.blue_filter {
  filter: invert(46%) sepia(51%) saturate(661%) hue-rotate(180deg)
    brightness(83%) contrast(96%);
}
</style>
