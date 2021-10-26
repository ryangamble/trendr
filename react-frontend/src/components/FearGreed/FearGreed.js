import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import axios from "axios";
import { Container } from "react-bootstrap";
import {
  XAxis,
  YAxis,
  HorizontalGridLines,
  FlexibleXYPlot,
  LineSeries,
  Crosshair,
  Borders,
  XYPlot,
  VerticalGridLines,
} from "react-vis";

function FearGreed() {
  const [graphData, setgraphData] = useState([]);
  const [fearGreedData, setFearGreedData] = useState([]);
  const [crosshairValues, setCrosshairValues] = useState([]);
  const currentTheme = useSelector((state) => state.theme.currentTheme);

  const _onMouseLeave = () => {
    setCrosshairValues([]);
  };

  const _onNearestX = (value) => {
    var x = value.x.toString();
    value.x = x;
    setCrosshairValues([value]);
  };

  useEffect(() => {
    const requestBody = {
      method: "get",
      headers: { "Content-Type": "application/json" },
    };

    axios
      .get("/assets/HistoricFearGreed", requestBody)
      .then((res) => JSON.parse(JSON.stringify(res.data)))
      .then((data) => {
        // get the first 30 historic fear greed data
        console.log(data);
        const arr = data.slice(0, 30).map((d) => {
          return {
            x: d.timestamp,
            y: d.value,
            z: d.value_classification,
          };
        });
        console.log(arr);

        setgraphData(arr);
      })
      .catch((err) => {
        alert(err);
      });
  }, []);

  return (
    <div>
      <Container align="center">
        <h3 style={{ color: currentTheme.foreground }}>
          Latest Fear and Greed Trends
        </h3>
        <FlexibleXYPlot
          onMouseLeave={_onMouseLeave}
          height={300}
          xType="ordinal"
        >
          <VerticalGridLines />
          <HorizontalGridLines />
          <XAxis hideTicks title="Latest 30 days" />
          <YAxis title="Fear Greed Index" />
          <LineSeries onNearestX={_onNearestX} data={graphData} color="blue" />
          <Crosshair
            values={crosshairValues}
            titleFormat={(d) => {
              console.log("d: ", d);
              return { title: "Date", value: d[0].x };
            }}
            itemsFormat={(d) => {
              console.log("d item: ", d);
              return [
                { title: "Index", value: d[0].y },
                { title: "Fear/Greed", value: d[0].z },
              ];
            }}
          />
        </FlexibleXYPlot>
      </Container>
    </div>
  );
}

export default FearGreed;
