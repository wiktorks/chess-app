import { FormEvent, useRef, useContext } from "react";
import { Button, Col, Container, Form, Row } from "react-bootstrap";

import { AuthContext } from "../../store/auth-context";

export const ProfileForm = () => {
  const oldPasswordInputRef = useRef<HTMLInputElement | null>(null);
  const newPasswordInputRef = useRef<HTMLInputElement | null>(null);
  const newPassword2InputRef = useRef<HTMLInputElement | null>(null);

  const authCtx = useContext(AuthContext);

  const submitHandler = (event: FormEvent) => {
    event.preventDefault();
    const enteredOldPassword = oldPasswordInputRef.current!.value;
    const enteredNewPassword = newPasswordInputRef.current!.value;
    const enteredNewPassword2 = newPassword2InputRef.current!.value;
    console.log(authCtx.token)
    fetch("http://0.0.0.0:8000/api/auth/password-reset/", {
      method: "PUT",
      body: JSON.stringify({
        old_password: enteredOldPassword,
        new_password: enteredNewPassword,
        new_password2: enteredNewPassword2,
      }),
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${authCtx.token}`,
      },
    })
      .then(async (res) => {
        if (res.ok) {
          return res.json();
        } else {
          let errorMessage = "Password reset failed failed!";
          throw new Error(errorMessage);
        }
      })
      .catch((err) => {
        alert(err.message);
      });
  };

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col md="5">
          <h1>Change password for Your account.</h1>
          <Form onSubmit={submitHandler}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Old Password</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter Old password"
                ref={oldPasswordInputRef}
                required
              />
              <Form.Label>New Password</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter New password"
                ref={newPasswordInputRef}
                required
              />
              <Form.Label>Confirm new password</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter New password"
                ref={newPassword2InputRef}
                required
              />
            </Form.Group>
            <Row className="justify-content-md-center">
              <Col md="6">
                <Button variant="primary" type="submit">
                  Change password
                </Button>
              </Col>
            </Row>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};
