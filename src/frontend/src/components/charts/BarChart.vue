<script>
import { Bar } from "vue-chartjs";

export default {
  extends: Bar,
  props: {
    data: Array,
    label: {
      type: String,
      default: "",
    },
  },
  mounted() {
    this.renderChart(
      {
        labels: this.data.map((x) => x.key),
        datasets: [
          {
            label: this.label,
            data: this.data.map((x) => x.count),
            backgroundColor: [
              "rgb(54, 162, 235)",
              "rgb(255, 205, 86)",
              "rgb(255, 99, 132)",
              "rgb(102, 187, 106)",
              "rgb(171, 71, 188)",
              "rgb(109, 76, 65)",
            ],
          },
        ],
      },
      {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false,
        },
      }
    );
  },
};
</script>
