import React from "react";
import { Container, Row, Col } from "react-bootstrap";

export default function PrivacyPolicy() {
  const brandColor = "#c3d831";

  return (
    <Container className="py-5">
      <Row>
        <Col lg={10} className="mx-auto">
          <h1 className="mb-4" style={{ color: brandColor }}>
            Privacy Policy
          </h1>
          <div className="content">
            <section className="mb-4">
              <h2 className="h4 mb-3">1. Demo Status</h2>
              <p>
                This repository is a portfolio release of an academic capstone
                project. It is provided for demonstration purposes and is not a
                production service.
              </p>
            </section>

            <section className="mb-4">
              <h2 className="h4 mb-3">2. Uploaded Data</h2>
              <ul>
                <li>Files you upload are processed to train models, generate predictions, or build dashboard views</li>
                <li>Uploaded data may be stored in the local project database while the application is running</li>
                <li>This public repository does not include a hosted data retention or account management system</li>
              </ul>
            </section>

            <section className="mb-4">
              <h2 className="h4 mb-3">3. Privacy Expectations</h2>
              <p>
                Do not upload confidential, regulated, or personally sensitive
                information to demo environments unless you control the
                deployment and understand how the data is being stored.
              </p>
            </section>

            <section className="mb-4">
              <h2 className="h4 mb-3">4. Third-Party Context</h2>
              <ul>
                <li>This portfolio release is an independent, sanitized publication of a prior capstone project</li>
                <li>Any references to prior collaborators or project context are informational only</li>
                <li>This repository is not presented as an official product or endorsed service of any outside organization</li>
              </ul>
            </section>

            <section className="mb-4">
              <h2 className="h4 mb-3">5. Contact</h2>
              <p>
                Questions about this portfolio release can be directed through
                the repository owner&apos;s preferred public contact channel.
                <br />
              </p>
            </section>

            <section className="mb-4">
              <h2 className="h4 mb-3">6. Updates to This Policy</h2>
              <p>
                This page may be updated as the repository evolves or as the
                public release is refined.
              </p>
            </section>

            <div className="mt-4 text-muted">
              <p>Last Updated: {new Date().toLocaleDateString()}</p>
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
}
