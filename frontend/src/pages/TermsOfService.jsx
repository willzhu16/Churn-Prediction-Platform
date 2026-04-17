import React from "react";
import { Container, Row, Col } from "react-bootstrap";

export default function TermsOfService() {
  const brandColor = "#c3d831";

  return (
    <Container className="py-5">
      <Row>
        <Col lg={10} className="mx-auto">
          <h1 className="mb-4" style={{ color: brandColor }}>
            Terms of Use
          </h1>
          <div className="content">
            <section className="mb-4">
              <h2 className="h4 mb-3">1. Demo Project</h2>
              <p>
                This application is published as a portfolio and demonstration
                project. It is not offered as a production service or official
                commercial platform.
              </p>
            </section>

            <section className="mb-4">
              <h2 className="h4 mb-3">2. Permitted Use</h2>
              <p>
                Use of the source code is governed by the repository license.
                If you interact with a live deployment, use it for evaluation,
                learning, and portfolio review purposes.
              </p>
              <ul>
                <li>Do not upload data you do not have permission to use</li>
                <li>Do not represent this project as an official third-party product</li>
                <li>Do not rely on this demo as a substitute for production-grade review or compliance processes</li>
              </ul>
            </section>

            <section className="mb-4">
              <h2 className="h4 mb-3">3. User Responsibilities</h2>
              <ul>
                <li>Review the code and deployment setup before using it with real data</li>
                <li>Use the application in compliance with applicable laws and data policies</li>
                <li>Treat model outputs as analytical assistance rather than guaranteed business decisions</li>
              </ul>
            </section>

            <section className="mb-4">
              <h2 className="h4 mb-3">4. Non-Affiliation</h2>
              <p>
                This repository is an independently published, sanitized
                portfolio release of a prior academic project. Any references to
                past project context are informational only and do not imply
                sponsorship, endorsement, or ongoing affiliation with any
                outside organization.
              </p>
            </section>

            <section className="mb-4">
              <h2 className="h4 mb-3">5. Disclaimer</h2>
              <p>
                The project is provided &quot;as is&quot; without warranties of
                any kind. The repository owner is not responsible for losses,
                damages, or compliance issues arising from use of the code or
                any self-hosted deployment.
              </p>
            </section>

            <section className="mb-4">
              <h2 className="h4 mb-3">6. Contact</h2>
              <p>
                Questions about this portfolio release should be directed
                through the repository owner&apos;s public contact channel.
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
