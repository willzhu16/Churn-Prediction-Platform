import React from "react";
import { Container, Row, Col, Alert } from "react-bootstrap";

export default function Contact() {
  const brandColor = "#c3d831";

  return (
    <Container className="py-5">
      <Row>
        <Col lg={10} className="mx-auto">
          <h1 className="mb-4" style={{ color: brandColor }}>
            Contact
          </h1>

          <Alert variant="secondary">
            This page is included for portfolio completeness. The demo does not
            currently provide a live contact form or support channel.
          </Alert>

          <Row className="mt-4">
            <Col md={8}>
              <div className="mb-4">
                <h3 className="h5 mb-3">About This Release</h3>
                <p>
                  This repository is a public portfolio edition of an older
                  university capstone project. Branding, deployment details, and
                  supporting pages were simplified to make the release safer and
                  easier to review.
                </p>
              </div>

              <div className="mb-4">
                <h3 className="h5 mb-3">How To Reach Out</h3>
                <p>
                  If you want to discuss the project, the best path is through
                  the repository owner&apos;s GitHub profile, portfolio site, or
                  other public professional contact channel.
                </p>
              </div>

              <div>
                <h3 className="h5 mb-3">What To Expect</h3>
                <p>
                  This demo is intended to showcase system design, model
                  training workflows, dashboard generation, and dynamic feature
                  handling. It is not maintained as a customer-facing product.
                </p>
              </div>
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
}
