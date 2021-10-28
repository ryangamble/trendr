import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";

import { Button } from "react-bootstrap";

// A reusable follow botton component that takes the stock/crypto id as props

function FollowBtn({ id }) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  //current user
  const currentUser = useSelector((state) => state.user);
  // a followed flag to indicate whether the current user follows the stock/crypto
  const [followed, setFollowed] = useState(false);

  const handleFollow = (e) => {
    e.preventDefault();

    //send follow/unfollow request to backend
    if (followed) {
      console.log("Unfollowing ", id);
    } else {
      console.log("Following ", id);
    }

    //toggle between follow/unfollow
    setFollowed(!followed);
  };

  useEffect(() => {
    //If the user is not logged in, return
    if (currentUser.username === "" && currentUser.email === "") return;

    // First Page Initial Mount, fetch whether the user follows this stock/crypto
    console.log(
      "fetching from backend to see whether the user follows this stock...",
      id
    );
  }, []);

  return (
    <div>
      <Button variant={currentTheme.variant} onClick={handleFollow}>
        {followed ? "Unfollow" : "Follow"}
      </Button>
    </div>
  );
}

export default FollowBtn;
