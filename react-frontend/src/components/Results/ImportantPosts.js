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
            // TODO: Add a check for twitter/reddit
            let embedUrl = post
            embedUrl = embedUrl.replace('www.reddit.com', 'www.redditmedia.com')
            embedUrl = embedUrl.substring(0, embedUrl.lastIndexOf('/', embedUrl.length - 2))
            embedUrl += '?ref_source=embed&amp;ref=share&amp;embed=true'
            console.log(`EMBED URL: ${embedUrl}`)
            return (
              <iframe key={i} src={embedUrl} height="599" width="640" />
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
