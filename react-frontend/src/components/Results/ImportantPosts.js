import React, { useEffect } from 'react'

import {
  Button,
  Modal
} from 'react-bootstrap'

function ImportantPosts (props) {
  useEffect(() => {
    // console.log(props)
  }, [props])

  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          Important Posts
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h4>{props.type && props.type}</h4>
        {
          props.posts &&
          props.posts.map((post, i) => {
            return (
              <a key={i} href={post}>{post}</a>
            )
          })
        }
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={props.onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  );
}

export default ImportantPosts
