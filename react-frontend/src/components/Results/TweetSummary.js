import React, { useEffect, useState } from 'react'
import { Row, Container, Spinner, Col, Table } from 'react-bootstrap'
import { useSelector } from 'react-redux'
import axios from 'axios'
import './Results.css'

function TweetSummary (props) {
  const currentTheme = useSelector((state) => state.theme.currentTheme)

  const [summaryData, setSummaryData] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    axios
      .get('http://localhost:5000/assets/tweet-summary/' + props.symbol)
      .then((res) => {
        setLoading(true)
        return JSON.parse(JSON.stringify(res.data))
      })
      .then((data) => {
        setSummaryData({
          minFollowers: data.follower_stats.min,
          medianFollowers: data.follower_stats.median,
          maxFollowers: data.follower_stats.max,
          minFollowing: data.following_stats.min,
          medianFollowing: data.following_stats.median,
          maxFollowing: data.following_stats.max,
          minAccountAge: data.accounts_age_stats.min,
          medianAccountAge: data.accounts_age_stats.median,
          maxAccountAge: data.accounts_age_stats.max,
          verifiedCount: data.verified_count
        })
      })
      .then(() => {
        setLoading(false)
      })
      .catch((error) => {
        console.log(error)
      })
  }, [])

  if (loading) {
    return (
      <Container fluid>
        <Spinner animation="border" />
      </Container>
    )
  } else {
    return (
      <Container className="tweetSummaryContainer">
        <Row>
          <h2 className="chartTitle">Users Tweeting About {props.symbol}</h2>
        </Row>
        <Row>
          <Col>
            <Table size="sm" className="tweetSummaryTable" style={{ color: currentTheme.foreground }}>
              <tbody>
                <tr>
                  <td className="statName">Min Followers</td>
                  <td className="statValue">{summaryData.minFollowers}</td>
                </tr>
                <tr>
                  <td className="statName">Median Followers</td>
                  <td className="statValue">{summaryData.medianFollowers}</td>
                </tr>
                <tr>
                  <td className="statName">Max Followers</td>
                  <td className="statValue">{summaryData.maxFollowers}</td>
                </tr>
                <tr>
                  <td className="statName">Min Following</td>
                  <td className="statValue">{summaryData.minFollowing}</td>
                </tr>
                <tr>
                  <td className="statName">Median Following</td>
                  <td className="statValue">{summaryData.medianFollowing}</td>
                </tr>
                <tr>
                  <td className="statName">Max Following</td>
                  <td className="statValue">{summaryData.maxFollowing}</td>
                </tr>
              </tbody>
            </Table>
          </Col>
          <Col>
            <Table size="sm" className="tweetSummaryTable" style={{ color: currentTheme.foreground }}>
              <tbody>
                <tr>
                  <td className="statName">Min Account Age</td>
                  <td className="statValue">{summaryData.minAccountAge} days</td>
                </tr>
                <tr>
                  <td className="statName">Median Account Age</td>
                  <td className="statValue">{summaryData.medianAccountAge} days</td>
                </tr>
                <tr>
                  <td className="statName">Max Account Age</td>
                  <td className="statValue">{summaryData.maxAccountAge} days</td>
                </tr>
                <tr>
                  <td className="statName">Number Verified</td>
                  <td className="statValue">{summaryData.verifiedCount}</td>
                </tr>
              </tbody>
            </Table>
          </Col>
        </Row>
      </Container>
    )
  }
}

export default TweetSummary
