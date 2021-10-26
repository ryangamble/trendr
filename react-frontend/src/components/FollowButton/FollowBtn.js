import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";

import { Button } from "react-bootstrap";

// A reusable follow botton component that takes the stock/crypto id as props

function FollowBtn({ id, isFollow, callback }) {
  const currentTheme = useSelector((state) => state.theme.currentTheme);
  const currentUser = useSelector((state) => state.user);

  const [follow, setFollow] = useState(false);

  useEffect(() => {
    // do this only if user is logged in
    if (currentUser.email !== "" || currentUser.username !== "") {
      console.log("fetching user follow list");
      setFollow(isFollow);
      console.log("follwo is", follow);
    }
  }, [isFollow]);

  const handleFollow = (e) => {
    e.preventDefault();

    //send follow/unfollow request to backend
    if (follow) {
      console.log("Unfollowing... ", id);

      if (callback) {
        console.log("calling cb...");
        callback(id);
      }
    } else {
      console.log("Following... ", id);
    }

    //toggle between follow/unfollow
    setFollow(!follow);
  };

  return (
    <div>
      <Button variant={currentTheme.variant} onClick={handleFollow}>
        {follow ? "Unfollow" : "Follow"}
      </Button>
    </div>
  );
}

export default FollowBtn;
