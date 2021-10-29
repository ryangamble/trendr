import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import axios from "axios";
import { Container, Spinner } from "react-bootstrap";
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
  const [crosshairValues, setCrosshairValues] = useState([]);
  const [loading, setLoading] = useState(true);
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
    axios
      .get("http://localhost:5000/assets/historic-fear-greed")
      .then((res) => JSON.parse(JSON.stringify(res.data)))
      .then((data) => {
        // get the first 30 historic fear greed data

        const arr = data.slice(0, 30).map((d) => {
          return {
            x: d.timestamp,
            y: d.value,
            z: d.value_classification,
          };
        });

        setgraphData(arr);
        setLoading(false);
      })
      .catch((err) => {
        alert(err);
      });
  }, []);

  return (
    <div>
      <Container
        align="center"
        style={{
          background: currentTheme.background,
          color: currentTheme.foreground,
        }}
      >
        {loading ? (
          <div>
            <Spinner animation="border" />
            <h4>Loading Fear and Greed Info...</h4>
          </div>
        ) : (
          <div>
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
              <LineSeries
                onNearestX={_onNearestX}
                data={graphData}
                color="blue"
              />
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
          </div>
        )}
      </Container>
    </div>
  );
}

export default FearGreed;
