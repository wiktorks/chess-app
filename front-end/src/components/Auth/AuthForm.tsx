import { useState, useRef, FormEvent } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Container, Row, Col } from "react-bootstrap";

const AuthForm = () => {
  const userInputRef = useRef<HTMLInputElement | null>(null);
  const emailInputRef = useRef<HTMLInputElement | null>(null);
  const passwordInputRef = useRef<HTMLInputElement | null>(null);
  const password2InputRef = useRef<HTMLInputElement | null>(null);

  const [isLogin, setIsLogin] = useState(true);

  const switchAuthModeHandler = () => {
    setIsLogin((prevState) => !prevState);
  };

  const submitHandler = (event: FormEvent) => {
    event.preventDefault();

    const enteredEmail = emailInputRef.current!.value;
    const enteredPassword = passwordInputRef.current!.value;

    if (isLogin) {
      let a = 1;
    } else {
      const enteredLogin = userInputRef.current!.value;
      const enteredPassword2 = password2InputRef.current!.value;
      fetch("http://0.0.0.0:8000/api/auth/register/", {
        method: "POST",
        body: JSON.stringify({
          username: enteredLogin,
          email: enteredEmail,
          password: enteredPassword,
          password2: enteredPassword2,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      }).then((res) => {
        if (res.ok) {
        } else {
          res.json().then((data) => {
            console.log(data);
          });
        }
      });
    }
  };

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col md="5">
          <h1>{isLogin ? "Login" : "Register"}</h1>
          <Form onSubmit={submitHandler}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              {!isLogin ? (
                <>
                  <Form.Label>Your Username</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Enter username"
                    ref={userInputRef}
                    required
                  />
                </>
              ) : null}

              <Form.Label>Your Email</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                ref={emailInputRef}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Password"
                ref={passwordInputRef}
                required
              />
              {!isLogin ? (
                <>
                  <Form.Label>Confirm Password</Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="Password"
                    ref={password2InputRef}
                    required
                  />
                </>
              ) : null}
            </Form.Group>
            <Row className="justify-content-md-center">
              <Col md="6">
                <Button variant="primary" type="submit">
                  {isLogin ? "Login" : "Create Account"}
                </Button>
              </Col>
            </Row>
            <Row className="justify-content-md-center">
              <Col md="6">
                <Button type="button" onClick={switchAuthModeHandler}>
                  {isLogin
                    ? "Create new account"
                    : "Login with existing account"}
                </Button>
              </Col>
            </Row>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default AuthForm;
