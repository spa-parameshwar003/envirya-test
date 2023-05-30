import React, { useEffect, useState } from "react";
import axios from "../../interceptor/interceptor";
import "chartjs-adapter-moment";
import {
  Chart as ChartJS,
  TimeScale, //Import timescale instead of category for X axis
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  BarElement,
} from "chart.js";
import { Bar, Line } from "react-chartjs-2";
import moment from "moment";
import { FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import Loader from "../../utils/loader/Loader";
import { toast } from "react-toastify";

ChartJS.register(
  TimeScale, //Register timescale instead of category for X axis
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = () => {
  const [chartData, setChartData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [range, setRange] = React.useState(5);

  const fetchData = async (range) => {
    const data = await axios
      .get("/getReadings/" + range)
      .then((res) => res.data)
      .catch((e) => {
        toast.error("something went wrong!");
        return [];
      });

    return data;
  };

  useEffect(() => {
    setIsLoading(true);
    (async () => {
      let data = await fetchData(range);
      setChartData(data);
      setIsLoading(false);
    })();
  }, [range]);

  const handleChange = (event) => {
    setRange(event.target.value);
  };

  console.log("chart data", chartData);

  const options = {
    scales: {
      x: {
        type: "time",
        time: {
          unit: "minute",
          parser: function (date) {
            return moment(date);
          },
        },
      },
    },
  };

  const timeseries_data = {
    datasets: [
      {
        label: "univariate",
        data: chartData.filter((x) => x.type == "univariate"),
        backgroundColor: ["Red"],
        borderColor: "red",
      },
      {
        label: "multivariate",
        data: chartData.filter((x) => x.type == "multivariate"),
        backgroundColor: ["Purple"],
        borderColor: "purple",
      },
    ],
  };

  return (
    <div className="container chart-container overflow-scroll">
      {isLoading ? (
        <Loader />
      ) : (
        <div className="container mt-5">
          <FormControl className="mb-5 rangeInput">
            <InputLabel id="demo-simple-select-label">Range</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={range}
              label="Range"
              onChange={handleChange}
            >
              <MenuItem value={5}>5 M</MenuItem>
              <MenuItem value={10}>10 M</MenuItem>
              <MenuItem value={15}>15 M</MenuItem>
              <MenuItem value={20}>20 M</MenuItem>
              <MenuItem value={25}>25 M</MenuItem>
              <MenuItem value={30}>30 M</MenuItem>
              <MenuItem value={60}>1 H</MenuItem>
            </Select>
          </FormControl>

          <div className="row">
            <h4>Time Series Chart</h4>
            <Line data={timeseries_data} options={options} />
          </div>

          <div className="row mt-5">
            <h4>Bar Chart</h4>
            <Bar data={timeseries_data} options={options} />
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
