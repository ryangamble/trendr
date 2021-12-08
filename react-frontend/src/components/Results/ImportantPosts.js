import React, { useEffect } from 'react'
import { TwitterTweetEmbed } from 'react-twitter-embed'
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
          Important Posts {props.type && " from " + props.type}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {
          props.posts &&
          (props.type === 'Reddit'
            ? (
                props.posts.map((post, i) => {
                  let embedUrl = post
                  embedUrl = embedUrl.replace('www.reddit.com', 'www.redditmedia.com')
                  embedUrl = embedUrl.substring(0, embedUrl.lastIndexOf('/', embedUrl.length - 2))
                  embedUrl += '?ref_source=embed&amp;ref=share&amp;embed=true'
                  console.log(`EMBED URL: ${embedUrl}`)
                  return (
                  <>
                    <iframe
                      key={i}
                      src={embedUrl}
                      height="300"
                      width="100%"
                    />
                    <hr />
                  </>
                  )
                })
              )
            : (
                props.posts.map((post, i) => {
                  let embedUrl = post
                  embedUrl = embedUrl.substring(embedUrl.lastIndexOf('/') + 1)
                  console.log(post)
                  return (
                    <>
                      <TwitterTweetEmbed
                        key={i}
                        tweetId={embedUrl}
                        options={{ width: '100%' }}
                      />
                    </>
                  )
                })
              )
          )}
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={props.onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  );
}

export default ImportantPosts
