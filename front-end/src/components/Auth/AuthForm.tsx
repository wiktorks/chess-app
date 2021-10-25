import { useState, useRef, FormEvent, useContext } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Container, Row, Col } from "react-bootstrap";
import { AuthContext } from "../../store/auth-context";

const AuthForm = () => {
  const userInputRef = useRef<HTMLInputElement | null>(null);
  const emailInputRef = useRef<HTMLInputElement | null>(null);
  const passwordInputRef = useRef<HTMLInputElement | null>(null);
  const password2InputRef = useRef<HTMLInputElement | null>(null);

  const authCtx = useContext(AuthContext);

  const [isLogin, setIsLogin] = useState(true);

  const switchAuthModeHandler = () => {
    setIsLogin((prevState) => !prevState);
  };

  const submitHandler = (event: FormEvent) => {
    interface LoginFormSubmit {
      username: string;
      password: string;
      email?: string;
      password2?: string;
    }

    event.preventDefault();

    const enteredLogin = userInputRef.current!.value;
    const enteredPassword = passwordInputRef.current!.value;

    let url;
    let body: LoginFormSubmit;

    if (isLogin) {
      url = "http://0.0.0.0:8000/api/auth/token/";
      body = {
        username: enteredLogin,
        password: enteredPassword,
      };
    } else {
      const enteredEmail = emailInputRef.current!.value;
      const enteredPassword2 = password2InputRef.current!.value;
      url = "http://0.0.0.0:8000/api/auth/register/";
      body = {
        username: enteredLogin,
        email: enteredEmail,
        password: enteredPassword,
        password2: enteredPassword2,
      };
    }
    fetch(url, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(async (res) => {
        if (res.ok) {
          return res.json();
        } else {
          // const data = await res.json();
          let errorMessage = "Authentication failed!";
          throw new Error(errorMessage);
        }
      })
      .then((data) => {
        authCtx.login(data.access);
      })
      .catch((err) => {
        alert(err.message);
      });
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
                  <Form.Label>Your Email</Form.Label>
                  <Form.Control
                    type="email"
                    placeholder="Enter email"
                    ref={emailInputRef}
                    required
                  />
                </>
              ) : null}

              <Form.Label>Your Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username"
                ref={userInputRef}
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
