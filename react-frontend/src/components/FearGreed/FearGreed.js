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
    value.x = value.x.toString();
    setCrosshairValues([value]);
  };

  useEffect(() => {
    axios
      .get("http://localhost:5000/assets/historic-fear-greed")
      .then((res) => {
        let data = JSON.parse(JSON.stringify(res.data));

        // get the first 30 historic fear and greed values
        const arr = data["crypto_values"].slice(0, 30).map((d) => {
          return {
            x: d.timestamp,
            y: d.value,
            z: d.value_classification,
          };
        });

        setgraphData(arr);
        setLoading(false);
      })
      .catch((error) => {
        console.log(`ERROR: ${error}`);
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
            <h4>Loading Crypto Fear and Greed Info...</h4>
          </div>
        ) : (
          <div>
            <h3 style={{ color: currentTheme.foreground }}>
              Latest Crypto Fear and Greed Trends
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
                  return { title: "Date", value: d[0].x };
                }}
                itemsFormat={(d) => {
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