import { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true);

  const switchAuthModeHandler = () => {
    setIsLogin((prevState) => !prevState);
  };

  return (
    <Form>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label>Email address</Form.Label>
        <Form.Control type="email" placeholder="Enter email" />
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Password" />
      </Form.Group>
      <Form.Group className="mb-3" controlId="formBasicCheckbox">
        <Form.Check type="checkbox" label="Check me out" />
      </Form.Group>
      <Button variant="primary" type="submit">
        Submit
      </Button>
    </Form>
    // <section className={classes.auth}>
    //   <h1>{isLogin ? "Login" : "Sign Up"}</h1>
    //   <form>
    //     <div className={classes.control}>
    //       <label htmlFor="email">Your Email</label>
    //       <input type="email" id="email" required />
    //     </div>
    //     <div className={classes.control}>
    //       <label htmlFor="password">Your Password</label>
    //       <input type="password" id="password" required />
    //     </div>
    //     <div className={classes.actions}>
    //       <button>{isLogin ? "Login" : "Create Account"}</button>
    //       <button
    //         type="button"
    //         className={classes.toggle}
    //         onClick={switchAuthModeHandler}
    //       >
    //         {isLogin ? "Create new account" : "Login with existing account"}
    //       </button>
    //     </div>
    //   </form>
    // </section>
  );
};

export default AuthForm;
