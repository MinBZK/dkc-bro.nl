<script>
import { Line } from "vue-chartjs";

export default {
  extends: Line,
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
        labels: [...new Set(this.data.map((x) => new Date(x.date).toLocaleDateString('en-GB')))],
        datasets: [
          {
            label: "Kwaliteitsregels geslaagd",
            data: this.data.map((x) => x.true),
            backgroundColor: "rgb(0, 200, 83)",
          },
          {
            label: "Kwaliteitsregels mislukt",
            data: this.data.map((x) => x.false),
            backgroundColor: "rgb(255, 23, 68)",
          },
        ],
      },
      {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              stacked: true,
            },
          ],
          yAxes: [
            {
              stacked: true,
              ticks: {
                min: Math.max(
                  Math.min(...this.data.map((x) => x.true)) - 20,
                  0
                ),
              },
            },
          ],
        },
      }
    );
  },
};
</script>
